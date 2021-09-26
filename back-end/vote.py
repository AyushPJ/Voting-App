from flask import Blueprint, request, jsonify, redirect, current_app
from flask.helpers import url_for
from flask.templating import render_template

from itsdangerous import SignatureExpired
from . import db
bp = Blueprint("vote", "vote", url_prefix="/vote")

@bp.route("/", methods=["POST"])
def submitVote():
    postReq = request.json
    if 'token' in postReq and  'votes' in postReq:
        token = postReq['token']
        s = current_app.config['serializer']
        try:
            email = s.loads(token,salt='confirm',max_age=1800)
        except SignatureExpired:
            return {'voteStatus': 3}
        votes = postReq['votes']
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("select voted from users where email=%s",(email,))
        voted = cursor.fetchone()
        if voted and voted[0]==False:
            postsVoted = dict()
            candidatesVoted = dict()
            validVote = True
            for vote in votes:
                cursor.execute("select c.roll_number, c.post from candidates c where c.roll_number = %s",(vote['rollNo'],))
                candidate = cursor.fetchone()
                if not candidate:
                    validVote = False
                    break
                if candidate[0] in candidatesVoted:
                    validVote = False
                    break
                if candidate[1] in postsVoted:
                    validVote = False
                    break
                candidatesVoted[candidate[0]] = True
                postsVoted[candidate[1]] = True
                cursor.execute("update candidates set votes = votes + 1 where roll_number = %s",(candidate[0],))
        else:
            validVote=False
        if validVote:
            cursor.execute("update users set voted=true where email=%s",(email,))
            conn.commit()
            return {'voteStatus': 1}
        
        else:
            return {'voteStatus': 2}
            
    return ("Invalid request format",400)
    
@bp.route("/votingUnsuccessful", methods=["GET"])
def votingUnsuccessful():
    return render_template('error_page.html')

@bp.route("/votingSuccessful", methods=["GET"])
def votingSuccessful():
    return render_template('vote_successful.html')

@bp.route("/tokenExpired",  methods=["GET"])
def tokenExpired():
    return render_template('token_expired.html')
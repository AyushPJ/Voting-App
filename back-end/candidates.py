from flask import Blueprint
from flask import request, jsonify

from . import db
bp = Blueprint("candidates", "candidates", url_prefix="/candidates")


@bp.route("/getPosts", methods=["GET"])
def getPosts():
    if (request.accept_mimetypes.best == "application/json"):
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("select distinct post from candidates");
        posts = [];
        for post in cursor.fetchall():
            posts.append(post[0])
        return jsonify(dict(posts = posts))
    else:
        return "invalid request", 404

@bp.route("/<post>", methods=["GET"])
def getCandidates(post):
    if (request.accept_mimetypes.best == "application/json"):
        post = post.split("%20")
        post = " ".join(post)
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("select c.roll_number, c.candidate_name, c.post, c.personal_caption from candidates c where c.post = %s",(post,))
        candidates = cursor.fetchall()
        return jsonify(dict(candidates = [dict(rollNo = rollNo, name = name, post = post, caption = caption) for rollNo, name, post, caption in candidates]))
    else:
        return "invalid request", 404
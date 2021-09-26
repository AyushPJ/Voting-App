from flask import Flask, request, redirect, render_template, url_for, send_from_directory
from flask_cors import CORS

from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired


def create_app():
    app = Flask("SAC-Election",static_url_path='',static_folder="front-end")
    CORS(app)

    app.config.from_pyfile('config.cfg')

    mail = Mail(app)

    s = URLSafeTimedSerializer('secret')
    
    app.config['serializer'] = s
    from . import db 
    db.init_app(app)

    from . import candidates
    app.register_blueprint(candidates.bp)

    from . import vote
    app.register_blueprint(vote.bp)


    # @app.route("/", methods=["GET"])
    # def index():
    #     return redirect("/vote/genSec")
        
    @app.route('/votingPage/token/<token>')
    def votingPage(token):
        return send_from_directory(app.static_folder,'index.html')

    @app.route('/')
    def login():
        return render_template('register.html')

    #@app.route('/vote')
    #def vote():

    @app.route('/register_validation', methods = ['POST'])
    def rvalidation():
        email = request.form.get('mail')

        validmail = email[-10:]

        if(validmail != "nitc.ac.in"):
            return "Invalid Email"

        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("select voted from users where email=%s",(email,))
        voted = cursor.fetchone()
        if voted and voted[0]==False:
        
            token = s.dumps(email,salt='confirm')
            sender = app.config['MAIL_USERNAME'][0]
            msg = Message('Confirm Email',sender=sender,recipients=[email])

            link = url_for('confirm_mail',token = token,_external=True)

            msg.body = 'Your link is {}'.format(link)
            mail.send(msg)
            return render_template('code_sent.html')
        
        else:
            return render_template('error_page.html')


    @app.route('/confirm/<token>')
    def confirm_mail(token):
        try:
            mail = s.loads(token,salt='confirm',max_age=1800)
            
        except SignatureExpired:
            return render_template('token_expired.html')
        return redirect(url_for('votingPage', token=token))

    return app
    

    
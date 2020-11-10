freefrom flask import Flask,request,url_for
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)
s = URLSafeTimedSerializer('sddeewfcvdee')

@app.route('/',methods  = ['GET','POST'])
def index():
    if request.method == 'GET' :
        return '<form action="/" method ="POST"> <input name = "email"><input type="submit"></form>'
    
    email = request.form['email']
    token = s.dumps(email,salt='email-confirm')  

    msg = Message('confirm eamil',sender = 'kenbazale@live.com',recipients=[email]) 

    link =  url_for('confirm_email',token = token,_external = True)
    msg.body = 'your link  is {}'.format(link)

    mail.send(msg)

    return 'the email you entered is {}. the token is {}'.format(email,token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
         email =s.load(token,salt= 'email-confirm',max_age =60)
    except SignatureExpired :
         return 'signature expired' 
    return'the token wotks'
if __name__ == "__main__":
    app.run(debug=True)
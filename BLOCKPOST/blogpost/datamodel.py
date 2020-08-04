from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from blogpost import db, login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),nullable=False)
    fname = db.Column(db.String(32),nullable=False)
    lname = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(124),unique=True,nullable=False)
    passwd = db.Column(db.String(64),nullable=False)
    profile_pic = db.Column(db.String(124),nullable=False,default='profile_pics/default.jpeg')
    posts = db.relationship('Post',backref='author',lazy=True)
    comments = db.relationship('Comment',backref='author',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None 
        return User.query.get(user_id)

    def __repr__(self):
        pass

    def like(self,post_id):
        pass

class Post(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    title = db.Column(db.String(255),nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_img = db.Column(db.String(124),nullable=False,default='post_imgs/00.jpeg')
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    num_ppl_seen = db.Column(db.Integer,nullable=False,default=0)
    num_comments = db.Column(db.Integer,nullable=False,default=0)
    num_ppl_liked = db.Column(db.Integer,nullable=False,default=0)
    comments = db.relationship('Comment',cascade="all,delete",backref='post',lazy=True)

class Comment(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    content = db.Column(db.Text,nullable=False)
    date_written = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    comment_img = db.Column(db.Text)

class Like_Seen(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    liked_or_seen = db.Column(db.String(64),nullable=False)  
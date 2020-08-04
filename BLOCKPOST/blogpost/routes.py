import secrets,os
from PIL import Image
from flask import render_template, url_for,redirect,flash,request,abort,session
from flask_login import current_user,login_user,logout_user,login_required
from flask_mail import Message
from blogpost.forms import (RegistrationForm,LoginForm,RequestResetForm,
                            ResetPasswordForm,PostForm,UpdateAccountForm,CommentForm)
from blogpost.datamodel import User,Post,Comment,Like_Seen,Comment
from blogpost import app,db,bcrypt,mail

def likes(post_id):
    likes = Like_Seen.query.filter_by(post_id=post_id).all()
    return len(likes)

def liked(post_id,user_id):
    like_ = Like_Seen.query.filter_by(post_id=post_id ,user_id=user_id).first()
    if(like_):
        return 'l'+str(post_id)
    return '-1'

def class_like(post_id,user_id):
    like_ = Like_Seen.query.filter_by(post_id=post_id ,user_id=user_id).first()
    if(like_):
        return "liked"
    return "notliked"

def num_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return len(comments)

@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=20)
    likes_ = Like_Seen.query.all()
    return render_template('home.html',posts=posts,likes=likes,liked=liked,num_comments=num_comments,class_like=class_like,str=str)

@app.route("/About")
def about():
    return render_template('about.html',title="About ShareYourStory")

@app.route("/register",methods=['GET','POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = RegistrationForm()
    if(form.validate_on_submit()):
        passwd_hash = bcrypt.generate_password_hash(form.passwd.data).decode('utf-8')
        user = User(username=form.username.data,fname=form.fname.data,lname=form.lname.data,email=form.email.data,passwd=passwd_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Successfully Created For {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title="Register",form=form)

@app.route("/login", methods=['GET' , 'POST'] )
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if(user and bcrypt.check_password_hash(user.passwd,form.passwd.data)):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Wrong Credentials','danger')
    return render_template('login.html', title='Login', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='cyberexpert2020@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To Reset Password, Follow The Link Below:
    {url_for('reset_token',token=token,_external=True)}'''
    mail.send(msg)

@app.route("/reset_passwd", methods = ['GET','POST'])
def request_reset():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = RequestResetForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email Sent To You For Password Reset','info')
        return redirect(url_for('login'))
    return render_template("reset_request.html",title="Password Reset",form=form)

@app.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if(user is None):
        flash("Link Invalid or Expired!!","warning")
        return redirect(url_for("reset_request.html"))
    form = ResetPasswordForm()
    if(form.validate_on_submit()):
        passwd_hash = bcrypt.generate_password_hash(form.passwd.data).decode('utf-8')
        user.passwd = passwd_hash
        db.session.commit()
        flash(f'Password Successfully Changed!!', 'success')
        return redirect(url_for('login'))
    return render_template("reset_token.html",title="Password Reset",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_pic(folder,form_pic):
    random_hex = secrets.token_hex(24)
    _,f_ext = os.path.splitext(form_pic.filename)
    pic_name = random_hex+f_ext
    pic_path = os.path.join(app.root_path,'static/'+folder,pic_name)
    img = Image.open(form_pic)
    w,h = img.size
    if(h>w):
        img=img.rotate(90,expand=True)
    #img.thumbnail(out_size,Image.ANTIALIAS)
    img.save(pic_path)
    img.close()
    return folder+pic_name

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    print(type(form.post_img.data))
    if(form.validate_on_submit()):
        img_post = save_pic("post_imgs/",form.post_img.data)
        post = Post(title=form.title.data,content=form.content.data,post_img=img_post,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Post Successfully Created' , 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html',title='New Post',form=form,legend='Post')

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if(form.validate_on_submit()):
        if(form.pic.data):
            pic_file = save_pic("profile_pics/",form.pic.data)
            current_user.profile_pic = pic_file
        current_user.username = form.username.data
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Successfully Updated Your Account",'success')
        return redirect(url_for('account'))
    elif(request.method == 'GET'):
        form.username.data = current_user.username
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.email.data = current_user.email
    img_file = url_for('static',filename=current_user.profile_pic)
    return render_template('account.html',title='Account',img_file=img_file,form=form)

@app.route("/like_seen/<int:post_id>/<int:user_id>/like_seen",methods=['POST','GET'])
def like_seen(post_id,user_id):
    like = Like_Seen.query.filter_by(user_id=user_id,post_id=post_id).first()
    if(like):
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like_Seen(post_id=post_id,user_id=user_id,liked_or_seen="like")
        db.session.add(like)
        db.session.commit()
    return '',204

@app.route("/comments/<int:post_id>/<int:user_id>/<int:page_num>/comment",methods=['GET','POST'])
def comment(post_id,user_id,page_num):
    form = CommentForm()
    if(form.validate_on_submit()):
        comment=Comment(post_id=post_id,user_id=user_id,content=form.content.data,comment_img="00.jpg")
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("home",page=page_num))
    return render_template("comment.html",form=form,legend="Comment")

@app.route("/comments/<int:post_id>",methods=['GET','POST'])
def comments(post_id):
    page = request.args.get('page',1,type=int)
    post = Post.query.filter_by(id=post_id).first()
    session['url'] = url_for('comments',post_id=post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_written.desc()).paginate(page=page,per_page=20)
    return render_template("comments.html",post=post,comments=comments,title="Post Comments")

@app.route("/home/posts/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html",title=post.title,post=post)

@app.route("/home/<string:option>/<int:post_id>",methods=['GET','POST'])
def delete(option,post_id):
    if(option == "post"):
        post = Post.query.get_or_404(post_id)
        if(post.author != current_user):
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash(f'Post Deletion Successful!','success')
    elif(option == "comment"):
        comment = Comment.query.get_or_404(post_id)
        if(comment.author != current_user):
            abort(403)
        db.session.delete(comment)
        db.session.commit()
        flash(f'Comment Deletion Successful!','success')
        if 'url' in session:
            return redirect(session['url'])
    return redirect(url_for('home'))

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if(post.author != current_user):
        abort(403)
    form = PostForm()
    if(form.validate_on_submit()):
        try:
            img_post = save_pic("post_imgs/",form.post_img.data)
            post.post_img = img_post
        except Exception as e:
            pass 
        finally:
            post.content = form.content.data
            post.title = form.title.data 
            db.session.commit()
        flash(f'Post Update Successful','success')
        return redirect(url_for('post',post_id=post.id))
    elif(request.method == 'GET'):
        form.title.data = post.title
        form.content.data = post.content
    return render_template("new_post.html",title='Update Post', form=form,legend='Post Update')

@app.route("/comments/<int:post_id>/<int:comment_id>/update",methods=['GET','POST'])
def comment_update(post_id,comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(post_id)
    if(comment.author != current_user):
        abort(403)
    form = CommentForm()
    if(form.validate_on_submit()):
        comment.content = form.content.data
        db.session.commit()
        flash(f'Comment Update Successful','success')
        if 'url' in session:
            return redirect(session['url'])
    elif(request.method == 'GET'):
        form.content.data = comment.content
    return render_template("comment.html",form=form,legend="Comment",comment=comment)

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page,per_page=2)
    author = User.query.filter_by(username=username).first()
    return render_template("user_posts.html",posts=posts,user=user,likes=likes,liked=liked,num_comments=num_comments,author=author,class_like=class_like,str=str)

@app.route("/home/admin/XYZ123/Laki/Mikia")
@login_required
def home_admin():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=20)
    likes_ = Like_Seen.query.all()
    return render_template('admin/admin_home.html',posts=posts,likes=likes,liked=liked,num_comments=num_comments,class_like=class_like,str=str)

@app.route("/comments/admin/admin/XYZ123/Laki/Mikia/<int:post_id>",methods=['GET','POST'])
def comments_admin(post_id):
    page = request.args.get('page',1,type=int)
    post = Post.query.filter_by(id=post_id).first()
    session['url'] = url_for('comments',post_id=post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_written.desc()).paginate(page=page,per_page=20)
    return render_template("admin/admin_comments.html",post=post,comments=comments,title="Post Comments")

@app.route("/home/admin/admin/XYZ123/Laki/Mikia/posts/<int:post_id>",methods=['GET','POST'])
def post_admin(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("admin/admin_post.html",title=post.title,post=post)
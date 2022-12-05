import os
import secrets
from PIL import Image
from flask import Flask, render_template,url_for, redirect, render_template, request, flash,abort,json
from models import User, Tweet,app,db,followers,Tweet_likes,Bookmarks
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

from handlers import EditProfile

# ----------------------------flask_login-------------------------------------------------
@app.route('/Home',methods=['GET'])
@login_required
def get_home():
        following= EditProfile()
        idx = following.home()
        return render_template("index.html",tweet=idx[6],user=current_user,img=idx[2],User_image=idx[7],user_like=idx[5],num_like=len(idx[0]),Tweets_like=idx[1],Bookmark=idx[3],Book_list=idx[4])
       

@app.route('/explore',methods=['GET'])
@login_required
def get_explore():
    return render_template('explore.html',user=current_user)

@app.route('/signUp',methods=['GET'])
def get_signUp():
    return render_template('/user_acaunt/signUp.html')

@app.route('/signIn',methods=['GET'])
def get_signIn():
    return render_template('/user_acaunt/signIn.html')    



@app.route('/signUp',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user:
        detected = check_password_hash( user.password, password )
        if detected:
            login_user(user)
            return redirect('/Home')
        else: 
            name = 'not password'
            return render_template('/user_acaunt/signUp.html',name=name)
   
    else:
        name = 'user not Faund'
        return render_template('/user_acaunt/signUp.html',name=name)


@app.route('/signIn',methods=['GET','POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hash = generate_password_hash(password)
    
    user = User.query.filter_by(email=email).first()
    r = User.query.filter_by(username=username).first()
    if user is not None:
        name = 'Please use a different email address.'
        return render_template('/user_acaunt/signIn.html',name=name)
    
    elif r is not None:
        name = 'User already exists.'
        return render_template('/user_acaunt/signIn.html',name=name)
    else:
        user = User(username=username,email=email,password=hash)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=email).first()
        login_user(user)
        return redirect('/signUp')
    

@app.route('/addTweet',methods=['POST'])
def sig_post():
        textarea = request.form['post']
        file = request.files['file']

        if file:
            img_post = save_picture(file)
            tweet = Tweet(title = "-", content = textarea,image_file=img_post,user_id = current_user.id)
            db.session.add(tweet)
            db.session.commit()
        else:    
            tweet = Tweet(title = "-", content = textarea,user_id = current_user.id)
            db.session.add(tweet)
            db.session.commit()
        return redirect("/Home")

@app.route('/Update_Acount',methods=['POST'])
def Update_Acount():
    file = request.files['file']

    if file:
        current_user.image_file = save_picture(file)
        db.session.commit()
    return redirect("/profile")

# ---------------------------------------
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/prifille_img', picture_fn)
    i = Image.open(form_picture)
    # output_size = (325, 325)
    # i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/')


# -------------------------------------------------

# @app.route('/addTweet/<int:id>/del')
# def delete_del(id):
#     tweet = Postr.query.get_or_404(id)
#     try:
#         db.session.delete(tweet)
#         db.session.commit()
#         return redirect('/Home')
#     except:
#         return "При удалении статьи произошла ошибка"


@app.route('/')
def index():
    return render_template("/user_acaunt/user_acaunt.html")


@app.route('/<int:id>',methods=['GET'])
@login_required
def profile_users(id):
    isUser = current_user
    if id == current_user.id:
        return redirect('/profile')
    else:
        profile = EditProfile()
        idx = profile.profile_data(id)
        tweet =Tweet.query.filter_by(user_id=idx[1].id).all()
        return render_template("profile/profile.html",isUser=idx[0], img = idx[2], date = idx[3], user_name = idx[1],tweet=tweet,user=idx[1],nums_following=idx[6],nums_followers=idx[5],id=idx[4],User_image=User,Bookmark = idx[9], Tweets_like = idx[10] )

# -----------------------------Profile----------------------------------------------------------------
@app.route('/followers$-<int:id>')
@login_required
def followers(id):
    followers= EditProfile()
    idx = followers.profile_data(id)
    return render_template("/profile/followers.html",isUser=idx[0],user_name=idx[1], img = idx[2],date = idx[3],followiers=idx[7],user = idx[1],nums_following = idx[6],nums_followers=idx[5],id = idx[4])


@app.route('/following$-<int:id>')
@login_required
def following(id):
    following= EditProfile()
    idx = following.profile_data(id)
    return render_template("/profile/following.html",isUser = idx[0],user_name=idx[1], img = idx[2],date=idx[3],following=idx[8],user=idx[1],nums_following=idx[6],nums_followers=idx[5],id=idx[4])



@app.route('/profile')
@login_required
def profile():
    id = current_user.id
    profile = EditProfile()
    idx = profile.profile(id)
    return render_template("/profile/profile.html",isUser=idx[0],user_name=idx[0],img = idx[2],date=idx[3],tweet=idx[6],user=idx[1],nums_following=idx[5],nums_followers=idx[4],id=id,User_image = User,Bookmark = idx[7],Tweets_like = idx[8] )

@app.route('/add_follow/<int:id>')
@login_required
def add_follow(id):

    user = User.query.get(id)
    if current_user.is_following(user):
        current_user.unfollow(user)
        db.session.commit()
    else:
        current_user.follow(user)
        db.session.commit()

    follow=current_user.is_following(User.query.get(id)) == True
    return json.dumps({'is':follow})

@app.route('/add_follow_profile/<int:id>')
@login_required
def add_follow_profile(id):

    user = User.query.get(id)
    if current_user.is_following(user):
        current_user.unfollow(user)
        db.session.commit()
    else:
        current_user.follow(user)
        db.session.commit()

    return redirect("/{}".format(id))
# ---------------------------------------------------------------
@app.route('/add_like/<int:id>')
@login_required
def add_like(id):
    user_like = Tweet_likes.query.filter_by(user_id=current_user.id).first()
    if user_like is None:
        likes = Tweet_likes(num_like = 0,tweet_id = id,user_id=current_user.id)
        db.session.add(likes)
        db.session.commit()

    else:
        Tweets_like = Tweet_likes.query.filter_by(user_id=current_user.id,tweet_id=id).first()
        if Tweets_like is None:
            likes = Tweet_likes(num_like = 0,tweet_id = id,user_id=current_user.id)
            db.session.add(likes)
            db.session.commit()
        else:
            db.session.delete(Tweets_like)
            db.session.commit()


    Tweets_like = Tweet_likes.query.filter_by(tweet_id=id).all()
    user_like = Tweet_likes.query.filter_by(user_id=current_user.id).first()  == None
    twt = Tweet_likes.query.filter_by(user_id = current_user.id,tweet_id = id).first() == None
    nums = len(Tweet_likes.query.filter_by(tweet_id=id).all())
    
    return json.dumps({'len': len(Tweets_like),'is':user_like, 'is2':twt,'nums':nums})

@app.route('/add_Bookmarks/<int:id>')
@login_required
def add_Bookmarks(id):
    user_Bookmarks = Bookmarks.query.filter_by(user_id=current_user.id).first()
    if user_Bookmarks is None:
        Bookmark = Bookmarks(tweet_id = id,user_id=current_user.id)
        db.session.add(Bookmark)
        db.session.commit()

    else:
        Bookmark = Bookmarks.query.filter_by(user_id=current_user.id,tweet_id=id).first()
        if Bookmark is None:
            Bookmark = Bookmarks(tweet_id = id,user_id=current_user.id)
            db.session.add(Bookmark)
            db.session.commit()
        else:
            db.session.delete(Bookmark)
            db.session.commit()

    return redirect("/Home")
# -------------------------------------------------------
@app.route('/nitification')
@login_required
def nitification():
    return render_template("nitification.html",user = current_user)

@app.route('/messanges')
@login_required
def messanges():
    return render_template("messanges.html",user=current_user)


@app.route('/bookmarks')
@login_required
def bookmarks():
    
    Bookmark = Bookmarks
    Book_list = Bookmark.query.filter_by(user_id = current_user.id).all()
    return render_template("bookmarks.html",Bookmark=Bookmark,Book_list=Book_list,user=current_user)

@app.route('/settings')
@login_required
def settings():
    return render_template("settings.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template('/errors/404.html'), 404

@app.errorhandler(401)
def not_found_error(error):
    return render_template('/errors/401.html'), 401

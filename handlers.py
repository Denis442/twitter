from models import User, Tweet,app,db,followers,Tweet_likes,Bookmarks
from flask_login import login_required, login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
class EditProfile():

    def home(self):
        like = Tweet_likes.query.order_by(Tweet_likes.tweet_id.desc()).all()
        Tweets_like = Tweet_likes
        Bookmark = Bookmarks
        Book_list = Bookmark.query.filter_by(user_id = current_user.id).all()
        user_like = Tweet_likes.query.filter_by(user_id=current_user.id).first()
        tweet = Tweet.query.order_by(Tweet.id.desc()).all()
        User_image = User
        image = current_user.image_file
        return [like,Tweets_like,image,Bookmark,Book_list,user_like,tweet,User_image]
    
    def profile(self, id):
        isUser = current_user
        Bookmark = Bookmarks
        image = current_user.image_file
        data_registration = current_user.date
        nums_following = len(current_user.followed.all())
        nums_followers = len(current_user.followers.all())
        tweet =Tweet.query.filter_by(user_id=current_user.id).all()
        user = User.query.filter_by(id=current_user.id).first()
        Tweets_like = Tweet_likes
        return [isUser,user,image,data_registration,nums_followers,nums_following,tweet,Bookmark,Tweets_like]

    def profile_data(self, id):
        Tweets_like = Tweet_likes
        Bookmark = Bookmarks
        isUser = current_user
        user= User.query.get(id)
        image = user.image_file
        date = user.date
        idx = id
        nums_followers = len(user.followers.all())
        nums_following = len(user.followed.all())
        followiers = user.followers.all()
        following = user.followed.all()
        return [isUser,user,image,date,idx,nums_followers,nums_following,followiers,following,Bookmark,Tweets_like]
       
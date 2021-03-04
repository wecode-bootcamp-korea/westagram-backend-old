from django.db import models

class User(models.Model):
    email           = models.EmailField(max_length=200, unique=True, verbose_name='Username')
    password        = models.CharField(max_length=300, verbose_name='Password') 
    nickname        = models.CharField(max_length=50)
    phone           = models.CharField(null=True, max_length=15)
    registered_time = models.DateTimeField(auto_now_add=True)
    updated_time    = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'

class UserFollow(models.Model):
    follower  = models.ForeignKey('User', related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey('User', related_name='following', on_delete=models.CASCADE) 
    
    class Meta:
        db_table = 'user_follow'



# class UserFollowing(models.Model):
#     user_id = models.ForeignKey("User", related_name="following")

#     following_user_id = models.ForeignKey("User", related_name="followers")

#     # You can even add info about when user started following
#     created = models.DateTimeField(auto_now_add=True)
# Now, in your post method implementation, you would do only this:

# UserFollowing.objects.create(user_id=user.id,
#                              following_user_id=follow.id)
# And then, you can access following and followers easily:

# user = User.objects.get(id=1) # it is just example with id 1
# user.following.all()
# user.followers.all()
   

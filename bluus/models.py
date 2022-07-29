from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """A class to represent a post made by a user"""
    caption=models.TextField( null=True, blank=True)
    pic=models.ImageField(upload_to = "post-pic/" ,null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(User, related_name="likes")
    num_of_likes=models.IntegerField(default=0)
    
    def __str__(self):
        """return a string representation of the model"""
        if len(self.caption)>119:
            return f"{self.caption[:120]}..."
        else:
            return self.caption
            
class Comment(models.Model):
    """A class to represent a comment made by a user."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment= models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(User, related_name="likes_comment")
    
    def __str__(self):
        """To return a string representation of  the comment text"""
        return self.comment

class Profile(models.Model):
    """A class to represent a user's' profile details"""
    
    GENDER_CHOICES=[('Male' ,'Male'), ('Female',  'Female')]
    RELATIONSHIP_CHOICES=[('Single','Single'), ('Married', 'Married'), ('In a relationship','In a relationship'),('Engaged', 'Engaged'), ("It's complicated", "It's complicated")]
    
    owner=models.ForeignKey(User,on_delete=models.CASCADE, related_name="profile")
    bio=models.CharField(max_length=90, blank=True)
    cover_photo=models.ImageField(upload_to="post-pic/",default='/post-pic/default_c_pic.jpg' ,blank=True)
    profile_pic=models.ImageField(upload_to="post-pic/",default='/post-pic/default_dp.png', blank=True)
    phone_num=models.BigIntegerField(null=True, blank=True)
    email=models.EmailField(blank=True)
    dob=models.DateField(blank=True, default='2000-01-01')
    city=models.CharField(max_length=30, blank=True)
    country=models.CharField(max_length=30, blank=True)
    #followers & following
    followers=models.ManyToManyField(User, related_name="follows")
    #gender
    gender=models.CharField(max_length=69, choices=GENDER_CHOICES, blank=True, null=True)
    #relationship_status
    relationship_status=models.CharField(max_length=69, choices=RELATIONSHIP_CHOICES, blank=True, null=True)
    
    def __str__(self):
        """return a string representation of a profile. """
        return self.owner.username

class Chat(models.Model):
    """A class to represent a  chat between two users"""
    #functiions like a list that holds the users that are involved in a chat
    participants=models.ManyToManyField(User, related_name="participates_in")
    
class Message(models.Model):
    """A class to represent a message by a user"""
    text=models.TextField()
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    date_sent=models.DateTimeField(auto_now_add=True)
    chat=models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="message")
    
    def __str__(self):
        """To return a string representation of  the message text"""
        if len(self.text)>30:
            return f"{self.text[:30]}..."
        else:
            return self.text
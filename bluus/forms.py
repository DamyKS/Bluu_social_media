from django import forms

from .models import Post, Comment, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption' , 'pic']
        labels = {'caption': 'Caption', 'pic': 'Photo'}
        widgets = {'caption': forms.Textarea(attrs={'cols': 5, 'rows': 3})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': 'comment'}
        widgets = {'comment': forms.Textarea(attrs={'cols': 30, 'rows':3})}

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['bio' , 'cover_photo', 'profile_pic', 'phone_num', 'email', 'dob', 'city', 'country', 'gender', 'relationship_status']
        labels={'bio': 'Bio' , 'cover_photo': 'Cover Photo', 'profile_pic': 'Profile Photo', 'phone_num': 'Phone(add country code, e.g 234)', 'Email': 'Email', 'dob': 'Date of birth(YYYY-MM-DD)', 'city': 'City', 'country':'Country', 'gender':'Gender', 'relationship_status': 'Relationship Status'}
        
        
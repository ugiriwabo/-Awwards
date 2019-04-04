from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Project(models.Model):
    image=models.ImageField(upload_to = 'images/')
    title = models.CharField(max_length =30)
    description=models.TextField(max_length =300)
    post_date = models.DateTimeField(auto_now=True)
    url=models.CharField(max_length =100)
    
    def __str__(self):
        return self.name
        
    def save_image(self):
        self.save() 

    @classmethod
    def get_image(cls,id):
        Image.objects.all()

    @classmethod
    def search_title(cls,search_term):
        titles=Project.objects.filter(title__icontains=search_term)
        return titles

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    username=models.CharField(max_length =30)
    profile_photo = models.ImageField(upload_to = 'pic/')
    bio=models.CharField(max_length =30)


    def save_profile(self):
        self.save() 
    
    @classmethod
    def get_profile(cls,id):
        Profile.objects.all()

    def delete_profile(self):
       self.delete()

    def update_bio(self,bio):
         self.bio=bio
         self.save()

    @classmethod
    def search_by_user(cls,search_term):
        user=Profile.objects.filter(name__icontains=search_term)
        users = cls.objects.filter(user=user)
        return users
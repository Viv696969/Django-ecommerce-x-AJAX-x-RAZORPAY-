from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    follows=models.ManyToManyField('self',related_name='followed_by',symmetrical=False,blank=True)
    #related name is exactly opposite of of what are data is
    # for example follows is how many people we follow but what if we want to acesss data of those users who follow us so we use related name


    def __str__(self):
        return self.user.username+'\t\t\t'+str(self.id)
    

# to automatically create a  user when  a  user signs up!!
# also to ensure user follows himself whhen he creates his account

def create_profile(sender,instance,created,**kwargs):
    if created:
        p=Profile(user=instance)
        p.save()
        p.follows.set([instance.profile.id])
        p.save()

post_save.connect(create_profile,sender=User)



class Tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=300,null=False,blank=False)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username+"      name->"+self.body
    
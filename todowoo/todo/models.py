from django.db import models
from django.contrib.auth.models import User
#Every class we create will represent a table name and all the data members we include will be the the column names 
"""
once we create a model we need to make a command 
python manage.py makemigrations  . will make a file of migrations
then
python manage.py migrate to make it push/migrate to the database

lastly just go to admin.py and register your models    admin.site.register(Model_name)

"""
# Create your models here.

class Todo(models.Model):
    title=models.CharField(max_length=50)
    memo=models.TextField(max_length=50,blank=True)

    date_created=models.DateTimeField(auto_now_add=True)
    date_completed=models.DateTimeField(null=True,blank=True)
    imp=models.BooleanField(default=False)   #for the checkbox if the user wants to mark it a imp he/she will click the checkbox and will be marked as true or false    but by default we set it as false bcoz it may/or may not be imp so will be on choice of user
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username+ '                     ' +str(self.date_created)
 
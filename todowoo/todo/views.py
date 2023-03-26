from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'home.html')



def signupuser(request):
    #whenever someone visits the signup page its a GET method as he/she is not passing any information throught the form and may be called as a guest 
    if request.method=='GET':   
        return render(request,'signup.html',{'form':UserCreationForm()}) 
        #we have to return a form object created by django made specially for signup
    else:
        if request.POST['password1']==request.POST['password2']:  #if both the passwords match then we have to create a user object through   User.objects.create_user() function
            
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                #after the user object is saved we have to redirect him to some page and then we use the redirect('html_page_name') function  and save it in the database

                #after we save we have to redirect the user to thhe login url 
                login(request,user)
                return redirect('currenttodos') #dont specify the .extension
            except IntegrityError:
                return render(request,'signup.html',{'form':UserCreationForm(),'error':'USERNAME HAS ALREADY BEEN TAKEN ENTER A NEW ONE '})

        else:
            return render(request,'signup.html',{'form':UserCreationForm(),'error':'PASSWORDS DIDNT MATCHED'})


@login_required
def currenttodos(request):
    todos=Todo.objects.filter(user=request.user,date_completed__isnull=True) #model_name__isnull=True will only show those todos which hhas field dat_completed as blnk/null
    
    return render(request,'currenttodos.html',{'todos':todos})

@login_required
def completed(request):
    todos=Todo.objects.filter(user=request.user,date_completed__isnull=False) #model_name__isnull=True will only show those todos which hhas field dat_completed as blnk/null
    
    return render(request,'completed.html',{'todos':todos})


def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method=='GET':   #when user gets to login page
        return render(request,'loginuser.html',{'form':AuthenticationForm()}) 
    else: # when user fills the details 
        user=authenticate(request,username=request.POST['username'],password=request.POST['password']); #checks if matches with database     if  doesnt find any match sends None value
        if user is None:  # when user details dnt mattch
            error='Username And Password didnt match';
            return render(request,'loginuser.html',{'form':AuthenticationForm(),'error':error})
        else:                               #when all is fine redirect to currenttodos page
            login(request,user)
            return redirect('currenttodos')

@login_required
def createtodo(request):
    if request.method=='GET':
        todoformobject=TodoForm();
        return render(request,'createtodo.html',{'form':todoformobject})
    else:
        try:
            form=TodoForm(request.POST)  #all the data entered in the form will be put in the form variable;
            newtodo=form.save(commit=False)  #will not save in database directly we can use to edit after
            newtodo.user=request.user
            newtodo.save()
            return redirect('currenttodos')
        except:
            return render(request,'createtodo.html',{'form':todoformobject,'error':'too big title'})

@login_required
def viewtodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user) # will give that todo for that particular primary key
    if request.method=='GET':
        print(todo.title+"\t\t"+todo.memo)
        form=TodoForm(instance=todo) #will get information in the form of that particular instance
        return render(request,'viewtodo.html',{'todo':todo,'form':form})
    else:
        try:
            form=TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except :
            return render(request,'viewtodo.html',{'todo':todo,'form':form,'error':'invalid data'})


def completetodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=='POST':
        todo.date_completed=datetime.now()
        todo.save()
        return redirect('currenttodos')

def deletetodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=='POST':
        todo.delete()
        return redirect('currenttodos')


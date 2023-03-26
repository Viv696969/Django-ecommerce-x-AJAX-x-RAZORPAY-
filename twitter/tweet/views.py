from random import shuffle
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
# for messages
from django.contrib import messages

# Create your views here.
def home(request):
    form=Tweetform()
    tweet=Tweet.objects.all().order_by('-created')
    context={'tweet':tweet,'form':form}

    if request.method=='GET':
        
        return render(request,'home.html',context)
    else:
        form=Tweetform(request.POST)
        t=form.save(commit=False)
        t.user=request.user
        t.save()
        messages.success(request,'your tweet is posted successfully')
        return redirect('home')


def profiles(request):
    p=Profile.objects.all()
    profile=list(p)  # convert model object to first list  to shuffle the  contents of the query set
    shuffle(profile)  # using the shuffle function random module
    print(profile)
    context={'profile':profile}
    return render(request,'profiles.html',context)

def profile(request,pk):
    prof=Profile.objects.get(id=pk)
    tweet=Tweet.objects.filter(user_id=pk).order_by('-created')
    context={'prof':prof,'tweet':tweet}
    if  request.user.is_authenticated:

        # that means if the user has clicked the follow / unfollow button
        if request.method=='POST':  
            # get the user who is  currently logged in and seeing the profiles
            current_user=request.user.profile
            status=request.POST['follow']
            if status=='unfollow':  # if the user presses the unfollow button

                # remove the profile from the users following
                current_user.follows.remove(prof)

            elif status=='follow':
                # add the profile to the users following
                current_user.follows.add(prof)
            
            current_user.save()

        

            

        return render(request,'profile.html',context)
    else:
        messages.warning(request,('You must be logged in to view this page'))
        return redirect('home')



def login_user(request):
    # to take input from the user
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        # to authenticate the user
        user=authenticate(request,username=username,password=password)
        # if the user is authenticated it wont refer none
        if user is not None:
            login(request,user)
            messages.success(request,'you have successfully logged in')
            return redirect('home')
        else:
            messages.error(request,'YOUR PASSWORD AND USERNAME DIDNT MATCHED   ENTER AGAIN')
            return render(request,'login.html',context={})

    else:
        return render(request,'login.html',context={})
    

def logout_user(request):
    logout(request)
    messages.warning(request,'you have logged out')
    return redirect('home')

def register_user(request):
    if request.method=='GET':
        return render(request,'register.html',{})
    else:
        uname=request.POST['username']
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        em=request.POST['email']
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        print(uname)
        print(pass1)
        print(pass2)
        print(em)
        print(fname)
        print(lname)

        if pass1==pass2:
            try:
                user=User.objects.create_user(username=uname,password=pass1,email=em,first_name=fname,last_name=lname)
                user.save()
                messages.success(request,'registeration successfull')
                return redirect('login')
            except:
                messages.error(request,'username already taken !! try new one')
                return render(request,'register.html',{})
            
        else:
            messages.error(request,'passwords didnt matched')
            return render(request,'register.html',{})
        

def update_user(request,pk):
    user=User.objects.get(id=pk)
    tweet=Tweet.objects.filter(user_id=pk)
    print(tweet)
    if request.method=='GET':
        context={'user':user}
        print(user)
        return render(request,'update_user.html',context)
    else:
        name=request.POST['test']
        print(name)
        return render(request,'update_user.html')


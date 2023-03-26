from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth.models import User
# for messages
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import *
# Create your views here.

def categories(request):
    
    return {'cat':Category.objects.all(),}

def home(request):
    if request.method=='GET':

        product=Product.objects.filter(status=True)



        context={'product':product}
        return render(request,'home.html',context)
    
def collections(request):
    if request.method=='GET':
        cat=Category.objects.all()
        context={'cat':cat}
        return render(request,'category.html',context)
    
def categorydetail(request,name):
    if request.method=='GET':
        cat=get_object_or_404(Category,name=name)
        product=Product.objects.filter(category=cat,status=True)
        context={'product':product}
        return render(request,'categorydetail.html',context)
    

def productview(request,id):
    
    product=get_object_or_404(Product,id=id)
    if request.method=='GET':
        context={'product':product}
        return render(request,'product.html',context)
    

def register_user(request):
    if  request.method=='GET':
        return render(request,'register.html')
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
                u=authenticate(request,username=uname,password=pass1)
                login(request,u)
                messages.success(request,'registeration successfull')
                return redirect('home')
            except:
                messages.error(request,'username already taken !! try new one')
                return render(request,'register.html',{})
            
        else:
            messages.error(request,'passwords didnt matched')
            return render(request,'register.html',{})

def login_user(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
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
        

def logout_user(request):
    logout(request)
    messages.warning(request,'you have logged out')
    return redirect('home')



def addtocart(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            product_id=int(request.POST['productid'])
            product_qty=int(request.POST['productqty'])
            print(product_id)
            print(product_qty)
            # messages.success(request,'working dnt wory')
            # return JsonResponse({})
            product=get_object_or_404(Product,id=product_id)
            # now check if the product is already in thecart
            if Cart.objects.filter(user=request.user,product_id=product_id): #if product already in cart
                messages.warning(request,'product already in cart')
                return JsonResponse({'mssg':'product already in cart'})
            else:
                # check if the quantity of the product is less
                if product.quantity >= product_qty:
                    # if true create the cart
                    cart=Cart.objects.create(user=request.user,product=product,quantity=product_qty)
                    cart.save()
                    messages.success(request,'cart created successfully')
                    return JsonResponse({'mssg':'cart created successfully'})
                else: #if the quantity available is less than the required quantity
                    messages.error(request,'Only {} left in stock'.format(product.quantity))
                    return JsonResponse({'mssg':'Only {} left in stock'.format(product.quantity)})
        else:
            messages.warning(request,'You need to login to add to cart')
            return JsonResponse({'mssg':'You need to login to add to cart'})
        
@login_required(login_url='login')
def cart(request):
    if request.method=='GET':
        cart=Cart.objects.filter(user=request.user)
        context={'cart':cart}
        return render(request,'cart.html',context)
    

def updatecart(request):
    if request.method=='POST':
        prodid=int(request.POST['productid'])
        prodqty=int(request.POST['productqty'])
        p=get_object_or_404(Cart,product_id=prodid,user=request.user)
        p.quantity=prodqty
        p.save()
        
        print(p)
        return JsonResponse({'mssg':'CART UPDATED'})
    

def deleteitem(request):
    if request.method=='POST':
        prodid=int(request.POST['productid'])
        prodqty=int(request.POST['productqty'])
        p=get_object_or_404(Cart,product_id=prodid,user=request.user)
        p.delete()
        return JsonResponse({'mssg':'ITEM DELETED'})
    

# ########################################   WISHLIST ##################################
@login_required(login_url='login')
def wishlist(request):
    list=Wishlist.objects.filter(user=request.user)
    context={'wishlist':list}
    return render(request,'wishlist.html',context)


@login_required(login_url='login')
def addtowishlist(request):
    if request.method=='POST':
        p_id=int(request.POST['productid'])
        print(p_id)
        if Wishlist.objects.filter(user=request.user,product_id=p_id):
            return JsonResponse({'mssg':'product already in  wishlist'})
        else:    
            w=Wishlist.objects.create(user=request.user,product_id=p_id)
            w.save()
            return JsonResponse({'mssg':'added to wishlist'})
        

def deletewishlistitem(request):
    if request.method=='POST':
        prod_id=int(request.POST['productid'])
        p=get_object_or_404(Wishlist,user=request.user,product_id=prod_id)
        p.delete()
        return JsonResponse({'mssg':'item removed from wishlist'})
    

def checkout(request):
    rawcart=Cart.objects.filter(user=request.user)
    for item in rawcart:  #delete all the items in cart whose quantity is greater than available stock
        if item.quantity > item.product.quantity:
            Cart.objects.delete(id=item.id)
        
    # now get the actual cart
    cart=Cart.objects.filter(user=request.user)
    total_price=0
    for item in cart:
        total_price=total_price + (item.product.selling_price * item.quantity) # tprice will be the atual price of product * the quantity the user reequested for

    # we also send the default details we had taken from the user
    p=Profile.objects.filter(user=request.user).first()
    

    context={'cart':cart,'total_price':total_price,'p':p}

    return render(request,'checkout.html',context)




import random
@login_required(login_url='login')
def placeorder(request):
    if request.method=='POST':
        prof=Profile.objects.filter(user=request.user).first()

        if not  prof:
            p=Profile()
            p.user=request.user
            p.first_name=request.POST['fname']
            p.last_name=request.POST['lname']
            p.email=request.POST['email']
            p.phone=request.POST['pno']
            p.address=request.POST['address']
            print(p.address)
            p.city=request.POST['city']
            p.state=request.POST['state']
            p.pin=request.POST['pin']
            p.save()


        o=Order()
        o.user=request.user
        o.f_name=request.POST['fname']
        o.l_name=request.POST['lname']
        o.email=request.POST['email']
        o.phone=request.POST['pno']
        o.address=request.POST['address']
        print(o.address)
        o.city=request.POST['city']
        o.state=request.POST['state']
        o.pin=request.POST['pin']
        o.payment_mode=mode=request.POST['paymentmode']
        if mode=='Razorpay':
            o.payment_id=request.POST['payid']
            print(o.payment_id)
        o.total_price=request.POST['totalprice']
        print(o.total_price)
        
        xyz=request.user.username+str(random.randint(11,99999))
        o.tracking_no=xyz
        o.save()
        # now we will get the cart items and store in the Orderitem table
        neworder=Cart.objects.filter(user=request.user)
        for item in neworder:
            OrderItem.objects.create(
                order=o,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.quantity
            )

            # to decrement the available stock

            orderproduct=Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity=orderproduct.quantity-item.quantity
            orderproduct.save()

        Cart.objects.filter(user=request.user).delete()
        messages.success(request,'Order Placed Successfully')

        if mode=='Razorpay':
            return JsonResponse({'mssg':'order placed successfully'})
        
        

        return redirect('home')

def yourorders(request):

    orders=Order.objects.filter(user=request.user)
    context={'orders':orders}
    return render(request,'yourorders.html',context)


def vieworder(request,pk):
    o=Order.objects.filter(id=pk,user=request.user).first()
    orderitem=OrderItem.objects.filter(order=o)
    context={'o':o,'orderitem':orderitem}
    return render(request,'vieworder.html',context)



def ajaxlist(request):
    p=Product.objects.filter(status=True).values_list('name',flat=True)
    productlist=list(p)
    return JsonResponse(productlist,safe=False)



def productsearch(request):
    if request.method=='POST':
        item=request.POST['prodsearch']

        if item==None:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product=Product.objects.filter(name__contains=item).first()
            if product:
                return redirect('product',product.id)
            else:
                messages.info(request,'No Such Product Found')
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))
            
    






    
    

       


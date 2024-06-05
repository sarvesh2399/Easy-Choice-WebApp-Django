from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from easychoiceapp.models import product, Cart, Order
from django.db.models import Q
import random
import razorpay
from .models import product

from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


def home(request):
    userid = request.user.id
    uname = request.user.username
    print("User id is: ", userid)
    print("Username: ", uname)
    print("Result is: ", request.user.is_authenticated)
    context={}
    p = product.objects.filter(is_active = True)
    context['products'] = p
    print(p)
    return render(request,'index.html', context)


def catfilter(request, cv):
    q1 = Q(is_active = True)
    q2 = Q(cat = cv)
    p = product.objects.filter(q1 & q2)
    print(p)
    context = {}
    context['products'] = p
    return render(request, 'index.html', context)



def pdetails(request, pid):
    p = product.objects.filter(id = pid)
    print(p)
    context = {}
    context['products'] = p
    return render(request, 'productDetails.html', context)


def addtocart(request, pid):
    if request.user.is_authenticated:
        userid = request.user.id
        # print(userid)
        # print(pid)
        u = User.objects.filter(id = userid)
        print(u[0])
        p = product.objects.filter(id = pid)
        print(p[0])
        q1 = Q(uid = u[0])
        q2 = Q(pid = p[0])
        c = Cart.objects.filter(q1 & q2)
        n = len(c)
        print(n)

        context ={}
        context['products'] = p
        if n==1:
            context['msg'] = "Product already exist in cart!"
            return render(request, 'productDetails.html', context)
        else:
            c = Cart.objects.create(uid = u[0], pid = p[0])
            c.save()
            
            context['success'] = "Product successfully added to the Cart!"
            context['products'] = p
            return render(request, 'productDetails.html', context) #cart (check once)
    else:
        return redirect('/login')


def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    np=len(orders)
    context['items']=np
    context['total']=s
    return render(request,'placeorder.html',context)

def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    print(c)       #It gives cart items added by user
    # print(c[0])
    # print(c[0].pid)
    # print(c[0].pid.name)
    # print(c[0].pid.price)
    s=0
    for x in c:
        print(x)             #Jeans|nike
        print(x.pid.price)    #800|10000
        s=s+x.pid.price*x.qty
    print(s)
    np=len(c)
    print(np)
    context ={}
    context['items'] = np
    context['total'] = s
    context['data'] = c
    return render(request, 'cart.html', context)
    
    

# def cart(request):
#     c=Cart.objects.filter(uid=request.user.id)
#     print(c)       #It gives cart items added by user
#     print(c[0])
#     print(c[0].pid)
#     print(c[0].pid.name)
#     print(c[0].pid.price)
#     s=0
#     for x in c:
#         print(x)             #Jeans|nike
#         print(x.pid.price)    #800|10000
#         s=s+x.pid.price*x.qty
    
#     print(s)
#     np=len(c)
#     print(np)
#     context ={}
#     context['items'] = np
#     context['total'] = s
#     context['data'] = c
#     return render(request, 'cart.html', context)

def ulogin(request):
    if request.method=="POST":
        uname = request.POST['uname']
        upass = request.POST['upass']
        print(uname,":", upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields cannot be empty"
            return render(request,'login.html', context)
        else:
            u=authenticate(username=uname, password=upass)
            # print(u)
            # print(u.username)
            # print(u.password)
            # print(u.is_superuser)
            if u is not None:
                login(request, u)  #Got error at this step - Resolved
                return redirect('/home')
            else:
                context['errmsg']="Invalid username/password"
                return render(request,'login.html', context)
                          
    else:
        return render(request, 'login.html')

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        print(uname,upass,ucpass)
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="Pass and confirm pass not matching"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User registered Successfully! Please go ahead and login!"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User already Registered,use a different Id!"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')


def updateqty(request, qv, cid):
    c = Cart.objects.filter(id=cid)
    if qv == '1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/cart')

# def remove(request, uid, source_page):
#     c = Cart.objects.filter(id=uid)
#     c.delete()
#     if source_page == 'cart':
#         return redirect('/cart')
#     elif source_page == 'placeorder':
#         return redirect('/placeorder')
#     else:
#         # Handle invalid source_page value, perhaps redirect to a default page
#         pass


def remove(request, uid):
    c = Cart.objects.filter(id=uid)
    c.delete()
    return redirect('/cart')

def remove_cart(request, uid):
    c = Order.objects.filter(id=uid)
    c.delete()
    return redirect('/placeorder')

# def remove_placeorder(request, uid):
#     c = Cart.objects.filter(id=uid)
#     c.delete()
#     return redirect('/placeorder')


# def profile(request):
#     # userid=request.user.id
#     # c=Cart.objects.filter(uid=userid)

#     userid=request.user.id
#     c=Cart.objects.filter(uid=userid)
#     orders=Order.objects.filter(uid=userid)
#     return render(request,'profile.html')


    # if request.user.is_authenticated:
    #     username = request.user.id
    #     email = request.user.id
        
    #     context = {
    #         'username': username,
    #         'email': email
    #     }
    #     return render(request, 'profile.html', context)
    # else:
    #     return redirect('/login')  

def ulogout(request):
    logout(request)
    return redirect('/home')


def profile(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    context={}
    context['data']=c
    return render(request,'profile.html')

def makepayment(request):

    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np = len(orders)
    # oid=x.order_id
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
        
    client = razorpay.Client(auth=("key", "pass"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    uemail=request.user.username
    context['uemail']=uemail
    return render(request, 'pay.html', context)

def search(request):
    query = request.GET.get('search')
    context = {}
    if query:
        results = product.objects.filter(Q(name__icontains=query) & Q(is_active=True))
        context['products'] = results
        context['search_query'] = query  # Optional: to display the search query on the page
    else:
        context['products'] = product.objects.filter(is_active=True)
    return render(request, 'index.html', context)

# def search(request):

#     return HttpResponse("Hey I am Search")


# def search(request):
#     query = request.GET.get('search')
#     print("Search Query:", query)
    
#     if query:
#         results = product.objects.filter(name__icontains=query, is_active=True)
#         print("Search Results:", results)
#         context = {'results': results, 'query': query}
#         print("Context Data:", context)
#         # return render(request, 'search.html', context)
#     else:
#         context = {'results': None, 'query': None}
#     return render(request, 'search.html', context)


def sendusermail(request):
    send_mail(
        "EasyChoice - Order Placed Successfully!",
        "Hey There, Order Placed! Shop With Us Again!",
        "sarveshspatil99@gmail.com",
        ["sarveshspatil77@gmail.com"],
        fail_silently=False,
    )
    return redirect('/home')
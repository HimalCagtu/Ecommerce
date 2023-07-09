from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm,LoginForm
from .models import *
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.db.models import Q, F, Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
# Create your views here.
def signup_form(request):
    if request.user.is_authenticated:
        return redirect('home')
    page = 'signup'
    form = UserForm()
    context = {'form': form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid:
            obj =  form.save(commit=False)
            
            obj.password = make_password(request.POST.get('password'))
            obj.save()
            return redirect('home')
        

    return render(request, 'form.html',{'form':form,'page':page,'title':'signup'})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email = email)

        except:
            return HttpResponse('User does not exist')

        user = authenticate(request,email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')


    return render(request, 'form.html',{'title':'login'})

def logoutpage(request):
 
    logout(request)

    

def homepage(request):
    query = request.GET.get('q') if request.GET.get('q')!= None else ''
    product = Product.objects.filter(Q(name__icontains =query) | Q(category__icontains =query)).order_by('-price') 
    
    alls = Product.objects.all()
    
    context = {'product':product,'user':request.user,'alls':alls, 'title':'home'}
    

    return render(request,'home.html',context)


@login_required(login_url='login')
def cart(request,pk):
    
    if request.user.is_authenticated:
        item = get_object_or_404(Product, id =pk)
        
        if item.quantity >= 1:
            order_item, created = Cart.objects.get_or_create(user = request.user , item = item , is_active=True)
         
        order_qs =Order.objects.filter(user = request.user , ordered = False)

        if order_qs.exists():
            order = order_qs[0] 

            if order.orderitems.filter(item = item).exists():
                if item.quantity >=1:
                    order_item.quantity += 1
                    item.quantity -=1
                    item.save()
                    order_item.save()
                    messages.info(request,'added successfully,.,,' )
                    return redirect('cartview')
                else:
                    messages.info(request, "Out of stock")
                    return redirect('home')
           
            else:
                if item.quantity >= 1:
                    order.orderitems.add(order_item)
                    item.quantity -=1
                    item.save()
                    messages.info(request,'added successfullyfad')
                    return redirect('cartview')
                else:
                    messages.info(request, "Out of stock")
                    return redirect('home')
           

        else:
            if item.quantity >=1:
                order = Order.objects.create(user = request.user)
                item.quantity -=1
                item.save()
                order.orderitems.add(order_item)
                messages.info(request,'added successfullydada')
                return redirect('cartview')
            else:
                messages.info(request, "Out of stock")
                return redirect('home')
           

        

def remove(request,pk):
    
    if request.user.is_authenticated:
        item = Product.objects.get(id = pk)

        cart_qs = Cart.objects.filter(user = request.user, item = item)

        if cart_qs.exists():
                cart = cart_qs[0]
                if cart.quantity <=1:
                    item.quantity +=1
                    item.save()
                    cart.delete()

                else:
                    cart.quantity -=1
                    item.quantity +=1
                    item.save()
                    cart.save()

        
        order_qs = Order.objects.filter(user = request.user, ordered = False)

        if order_qs.exists():
            order = order_qs[0]

            if order.orderitems.filter(item = item).exists():
                order_item = Cart.objects.filter(item = item , user = request.user)[0]
                order.orderitems.remove(order_item)

                return redirect('cartview')
            
            else:
                return redirect('cartview')


    else:
        return redirect('cartview')

@login_required(login_url='login')
def cart_view(request):
    cart = Cart.objects.filter(user =request.user, is_active=True).annotate(p = F('quantity') * F('item__price'))
    page = 'cartview'

   



    order_cart = Order.objects.filter(user = request.user , ordered =False) 
    ordered = Order.objects.filter(user=request.user, ordered=True)
   
    # total = order_cart[0].orderitems.count
    context ={
        
        'cart':cart,
        'p':cart.aggregate(Sum('p'))['p__sum'],
        'title' : 'cart',
        'page' : page,
        'ordered':ordered,
    }


    return render(request,'cart.html',context)


@login_required(login_url='login')
def shipping(request):

    page = 'shipping'
    form = ShippingForm()
    cart = Cart.objects.filter(user =request.user, is_active=True).annotate(p = F('quantity') * F('item__price'))
    

    order_cart = Order.objects.get(user = request.user , ordered =False)
    
    total = order_cart.orderitems.count
    context ={'page':page,
              'form':form,
              'total':total,
              'cart':cart,
              'p':cart.aggregate(Sum('p'))['p__sum'],
              'title': 'shipping'
             }
    
    if request.method == 'POST':
        update = Order.objects.filter(user=request.user, ordered=False).update(ordered=True)
        
        form = ShippingForm(request.POST)
        if form.is_valid():
            cart.update(is_active=False)
            
            obj =form.save(commit=False)
            obj.user = request.user
            obj.order = order_cart
            obj.save()
            
            send_mail(
                "Purchase",
                "Thanks for purchasing products",
                "himlu.dada@gmail.com",
                [request.user.email],
                fail_silently=False,
            )
            

            
            
            return redirect('home')

    

    return render(request, 'cart.html',context)


def payment(request):
    # key = settings.STRIPE_PUBLISHABLE_KEY
    # order_qs = Order.objects.filter(user = request.user, ordered = False)
    # cart = Cart.objects.filter(user =request.user)
    # p =0
    
    # for i in cart:
    #    p += i.item.price * i.quantity

    # if request.method == 'POST':
    #     charge = stripe.Charge.create(amount = p)
    #     currency = 'usd',
    #     description = order_qs
    #     source = request.POST['stripeToken']


    
    return render(request, 'payment.html') 
# {'key':key,'total':p})

def removeitem(request, pk):
    # product = Product.objects.get(id = pk)
    item = Cart.objects.get(id =pk)
    
    # product.quantity += item.quantity
    # product.save()
    item.delete()
    return redirect('cartview')


def details(request, pk):
    item = Product.objects.get(id = pk)

    return render(request,'details.html',{'item':item})


def profile(request):

    user = User.objects.get(id =request.user.id)

    return render(request, 'profile.html', {'user':user})



def changepassword(request):
    page = 'changepassword'
    form = PasswordChangeForm(request.user)
    context = {'form':form,
               'page':page}

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
           user = form.save()
           update_session_auth_hash(request, user)
           return redirect('logout')
        
    return render(request,'profile.html',context)

def passwordresetcomplete(request):

    return redirect('login')



def updateprofile(request):
    page = 'update'
    form = UserUpdate(instance=request.user)
    context = {'page':page,
               'form':form,
            }
    
    if request.method == 'POST':

        form = UserUpdate(request.POST, request.FILES , instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')


    return render(request,'profile.html',context)
from django.shortcuts import render, redirect
from .forms import CarForm, RegisterForm
from .models import Car
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Payment
# Create your views here.
def index(request):
    return render(request, 'index.html')


def pay_now(request):
    if request.method == "POST":
        phone_number = request.POST['phone']
        amount = int(request.POST['amount'])
        account_reference = "safari-shop"
        transaction_description = "payment of school fees"
        callback_url = "https://safari-shop.onrender.com/callback/"
        cl = MpesaClient()
        response = cl.stk_push(phone_number, amount, account_reference, transaction_description, callback_url)
        print(response)
        #save payment details in db
        Payment.objects.create(phone_number=phone_number,amount=amount,status="pending",
                               merchant_id=response.merchant_request_id)
        return HttpResponse('payment initiated')

    return render(request, 'pay.html')


@csrf_exempt
def callback(request):
    if request.method == "POST":
        data=request.body
        print("callback data",data)
        return JsonResponse({'status':'success'})
    return JsonResponse({'status':'failure'})

# Create your views here.
def index(request):
    #fetch only 3
    cars = Car.objects.all()[:3]
    carousel_items = Car.objects.filter(image__isnull=False).exclude(image__exact='')[:3]
    return render(request, 'index.html', {'cars': cars, 'carousel_items': carousel_items})
#registering a user
def register_user(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()#saves to db the user
            return redirect('index')
    else:
        form=RegisterForm()    
    return render(request,'register.html',{'form':form})
def login_user(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if user.is_staff:
                return redirect('index')
            else:
                return redirect('user')
        
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})
@login_required(login_url='login')
def user_dashboard(request):
    cars=Car.objects.all()
    return render(request, 'users/user-dashboard.html', {'products': cars})
#logout 
def logout_user(request):
    logout(request)
    return redirect('login')
#R-read-fetch data from db and display in admin dashboard
@staff_member_required(login_url='login')
def admin(request):
    products=Car.objects.all()
    return render(request, 'admin dashboard.html',{'products':products})
#create-add data to db using forms
@staff_member_required(login_url='login')
def addproduct(request):
    if request.method == 'POST':
        form=CarForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = CarForm()
    return render(request, 'addproduct.html', {'form': form})
#D-delete data from db
@staff_member_required(login_url='login')
def delete_product(request,id):
    Car.objects.filter(id=id).delete()
    return redirect('products')
#u- update existing data in db
@staff_member_required(login_url='login')
def update_product(request,id):
    product=get_object_or_404(Car,id=id)
    if request.method=='POST':
        form = CarForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else :
        form=CarForm(instance=product)
        return render(request,'addproduct.html',{'form':form})



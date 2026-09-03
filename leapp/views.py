from django.shortcuts import render, redirect
from .forms import CarForm, RegisterForm
from .models import Car
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required,user_passes_test

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
    return render(request, 'users/users-dashboard.html',{'products':cars})
#logout 
def logout_user(request):
    logout(request)
    return redirect('login')
#R-read-fetch data from db and display in admin dashboard
@login_required(login_url='index.html')
@user_passes_test(lambda u:u.is_staff,login_url='login')
def admin(request):
    products=Car.objects.all()
    return render(request, 'admin dashboard.html',{'products':products})
#create-add data to db using forms
@user_passes_test(lambda u:u.is_staff,login_url='login')
@login_required(login_url='index.html')
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
@user_passes_test(lambda u:u.is_staff,login_url='login')
@login_required(login_url='login')
def delete_product(request,id):
    product=get_object_or_404(Car,id=id)
    product.delete()
    return redirect('cars')
#u- update existing data in db
@user_passes_test(lambda u:u.is_staff,login_url='login')
@login_required(login_url='login')
def update_product(request,id):
    product=get_object_or_404(Car,id=id)
    if request.method=='POST':
        form = CarForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('cars')
    else :
        form=CarForm(instance=cars)
        return render(request,'addproduct.html',{'form':form})

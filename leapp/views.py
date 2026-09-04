from django.shortcuts import render, redirect
from .forms import CarForm, RegisterForm
from .models import Car
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

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

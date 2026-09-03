from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='index'),
    path('register/',views.register_user,name='register'),
    path('login/',views.login_user,name='login'),
    path('user/',views.user_dashboard,name='user'),
    path('logout/',views.logout_user,name='logout'),
     path('products/',views.admin,name='products'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('delete/<int:id>/',views.delete_product,name='delete'),
    path('update/<int:id>/',views.update_product,name='update'),
]
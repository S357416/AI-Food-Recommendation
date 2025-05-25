"""assessment4_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from assessment4_app import views
from assessment4_app.views import food_log, waste_log

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('list/', views.Food_List, name='list'),
    path('data_model/', views.data_model, name='data_model'),
    path('login/', views.login_view, name='login'),
    re_path(r'^detail/(?P<detail_id>[1-5]{1})/?$', views.detail_single, name='detail_single'),
    
    path('add/user/', views.add_user, name='add_user'),
    path('add/user/done/', views.add_user_submit),
    re_path(r'^edit/user/(?P<user>\w+)/$', views.edit_user, name='edit_user'),
    re_path(r'^delete/user/(?P<user>\w+)/$', views.delete_user),

    path('add/fooditem/', views.add_fooditem, name='add_fooditem'),
    path('add/fooditem/done/', views.add_fooditem_submit),
    re_path(r'^edit/fooditem/(?P<foodname>\w+)/$', views.modify_fooditem),
    re_path(r'^delete/fooditem/(?P<foodname>\w+)/$', views.modify_fooditem),

    path('add/wasteaudit/', views.add_wasteaudit, name='add_wasteaudit'),
    path('add/wasteaudit/done/', views.add_wasteaudit_submit),
    re_path(r'^edit/wasteaudit/(?P<key>\d+)/$', views.modify_wasteaudit),
    re_path(r'^delete/fooditem/(?P<key>\d+)/$', views.modify_wasteaudit),

    path('food_log/', food_log, name='food_log'),
    re_path(r'^edit/fooditem/(?P<foodname>\w+)/$', views.edit_fooditem, name='edit_fooditem'),
    path('food_log/delete/<foodname>/', views.delete_food_item, name='delete_food_item'),

    path('waste_log/', waste_log, name='waste_log'),
    re_path(r'^edit/wasteaudit/(?P<key>\d+)/$', views.edit_wasteaudit, name='edit_wasteaudit'),
    path('waste_log/delete/<int:key>/', views.delete_waste_audit, name='delete_waste_audit'),
]

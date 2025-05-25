from django.shortcuts import render, get_object_or_404, redirect
from assessment4_app.models import User, FoodItem, WasteAudit
from assessment4_app.forms import UserForm, FoodItemForm, WasteAuditForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

import datetime
# Create your views here.

app_name = 'assessment4_app/'

def home(request):
    return render(request, 'assessment4_app/home.html')


def Food_List(request):
    context_data={
        'Food_1': 'Bread',
        'Food_2': 'Milk',
        'Food_3': 'Potatoes',
        'Food_4': 'Cheese',
        'Food_5': 'Bagged Lettuce',
    }

    return render(request, 'assessment4_app/list.html', context_data)



def detail_single(request, detail_id):

    id = int(detail_id)

    detail_list = create_detail()

    detail = None

    for item in detail_list:
        if item.id == id: 
            detail = item

    context_data = {
        'detail': detail
    }
    return render(request, 'assessment4_app/details.html', context_data)


# class definitions

class food:

    def __init__(self, id, name, type, bio, amount, decomptime,):
        self.id = id
        self.name = name
        self.type = type
        self.bio = bio
        self.amount = amount
        self.decomptime = decomptime

def create_detail():
    the_list = []

    the_list.append(food(1, 'Bread', 'Grains', True, '186,000 tonnes', '3-4 days',))
    the_list.append(food(2, 'Milk', 'Dairy', False, '1180 tonnes', '7 days',) )
    the_list.append(food(3, 'Potatoes', 'Fruit/Vegetables', True, '130,000 tonnes', '5-7 days',))
    the_list.append(food(4, 'Cheese', 'Dairy', True, '39 tonnes', '7 days',))
    the_list.append(food(5, 'Bagged Lettuce', 'Fruit/Vegetables', False, '4,474 tonnes', '25 years',))

    return the_list


def data_model(request):

    food_list = create_detail()
    
    id_example = food_list[0].id
    name_example = food_list[0].name
    type_example = food_list[0].type
    bio_example = food_list[0].bio
    amount_example = food_list[0].amount
    decomptime_example = food_list[0].decomptime
    
    id_type = type(id_example).__name__
    name_type = type(name_example).__name__
    type_type = type(type_example).__name__
    bio_type = type(bio_example).__name__
    amount_type = type(amount_example).__name__
    decomptime_type = type(decomptime_example).__name__

    id_length = name_length = type_length = bio_length = amount_length = decomptime_length = 0
    for food in food_list:
        id_length = max(id_length, len(str(food.id)))
        name_length = max(name_length, len(food.name))
        type_length = max(type_length, len(food.type))
        bio_length = max(bio_length, len(str(food.bio)))
        amount_length = max(amount_length, len(food.amount))
        decomptime_length = max(decomptime_length, len(str(food.decomptime)))

    context_data = {
        'id_type': id_type,
        'name_type': name_type,
        'type_type': type_type,
        'bio_type': bio_type,
        'amount_type': amount_type,
        'decomptime_type': decomptime_type,

        'id_length': id_length,
        'name_length': name_length,
        'type_length': type_length,
        'bio_length': bio_length,
        'amount_length': amount_length,
        'decomptime_length': decomptime_length,
        
        'id_constraint': 'primary',
        'name_constraint': 'not_null',
        'type_constraint': 'not_null',
        'bio_constraint': 'not_null',
        'amount_constraint': 'not_null',
        'decomptime_constraint': 'not_null',
        
        'id_description': 'An unique indentifier for the different type of food',
        'name_description': 'Commonly associated name of the food',
        'type_description': 'The type of food family that the food falls under',
        'bio_description': 'Is the food biodegradable meaning can the food be decomposed by bacteria',
        'amount_description': 'How much of the food is wasted each year',
        'decomptime_description': 'How long the food takes to decompose',
        
        'id_example': id_example,
        'name_example': name_example,
        'type_example': type_example,
        'bio_example': bio_example,
        'amount_example': amount_example,
        'decomptime_example': decomptime_example
        
    }
    return render(request, 'assessment4_app/data_model.html', context_data)

# add user

def add_user(request):

    page_data = {'myform': UserForm()}

    return render(request, app_name + 'add_user.html', page_data)

def add_user_submit(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/add/user/')
    else:
        page_data = {}
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, 'Invalid form data. Please check the fields.')
            page_data = {'myform': form}
    
    return render(request, app_name + 'add_user.html', page_data)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
    else:
        form = AuthenticationForm(request)
    
    return render(request, 'assessment4_app/login.html', {'form': form})

def edit_user(request, user):
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        messages.error(request, 'The specific user does not exist')
        return HttpResponseRedirect(reverse('homepage'))

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('homepage'))
        else:
            context_data = {
                'myform': form,
            }
    else:
        form = UserForm(instance=user)
        context_data = {
            'myform': form,
        }

    return render(request, app_name + 'edit_user.html', context_data)

def delete_user(request, key=1):
    user = User.objects.get(id=int(key))
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('homepage'))
    else:
        form = UserForm(instance=user)
        context_data = {
            'myform': form,
        }

    return render(request, app_name + 'delete_user.html', context_data)

# add food item

def add_fooditem(request):
    page_data = {'myform': FoodItemForm()}
    return render(request, app_name + 'add_fooditem.html', page_data)

def add_fooditem_submit(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/add/fooditem/')
    else:
        form = FoodItemForm(request.POST)
        if form.is_valid():
            save_new_fooditem(form)
            return HttpResponseRedirect(reverse('food_log'))
        else:
            messages.error(request, 'Invalid form data. Please check the fields.')
            page_data = {'myform': form}
    
    return render(request, app_name + 'add_fooditem.html', page_data)


def save_new_fooditem(form):
    new_fooditem_object = form.save()


def modify_fooditem(request, foodname):
    try:
        food_item = FoodItem.objects.get(food_name=foodname)
    except FoodItem.DoesNotExist:
        messages.error(request, 'The specified food item does not exist.')
        return HttpResponseRedirect(reverse('food_log'))
    
    page_data = None

    if request.method == 'POST':
        if 'edit' in request.POST:
            form = FoodItemForm(request.POST, instance=food_item)
            page_data = edit_fooditem(request, form)
        elif 'delete' in request.POST:
            page_data = delete_fooditem(food_item)
        return HttpResponseRedirect(reverse('food_log'))
    else:
        form = FoodItemForm(instance=food_item)
        page_data = {'myform': form}
    
    return render(request, app_name + 'edit_fooditem.html', page_data)

def edit_fooditem(request, form):
    page_data = {}
    
    if form.is_valid() != True:
        messages.error(request, 'Invalid form data. Please check the fields.')
        page_data = {'myform': form}
    else:
        form.save()
    
    return page_data

def delete_fooditem(food_item):
    food_item.delete()
    return None


# add waste audit

def add_wasteaudit(request):
    page_data = {'myform': WasteAuditForm()}
    return render(request, app_name + 'add_wasteaudit.html', page_data)


def add_wasteaudit_submit(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/add/wasteaudit/')
    else:
        page_data = {}
        form = WasteAuditForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('waste_log'))
        else:
            messages.error(request, 'Invalid form data. Please check the fields.')
            page_data = {'myform': form}
    
    return render(request, app_name + 'add_wasteaudit.html', page_data)

def modify_wasteaudit(request, key=1):
    try:
        wasteaudit = WasteAudit.objects.get(id=int(key))
    except WasteAudit.DoesNotExist:
        messages.error(request, 'The specified waste audit entry does not exist.')
        return HttpResponseRedirect(reverse('waste_log'))

    page_data = None

    if request.method == 'POST':
        if 'edit' in request.POST:
            form = WasteAuditForm(request.POST, instance=wasteaudit)
            page_data = edit_wasteaudit(form)
        elif 'delete' in request.POST:
            page_data = delete_wasteaudit(wasteaudit)
        return HttpResponseRedirect(reverse('waste_log'))
    else:
        form = WasteAuditForm(instance=wasteaudit)
        page_data = {'myform': form}

    return render(request, app_name + 'edit_wasteaudit.html', page_data)


def edit_wasteaudit(form):
    page_data = {}

    if form.is_valid() != True:
        page_data = {'myform': form}
    else:
        form.save()

    return page_data


def delete_wasteaudit(wasteaudit):
    wasteaudit.delete()
    return None


# food log

def food_log(request):
    food_log = FoodItem.objects.all()
    return render(request, app_name + 'food_log.html', {'food_log': food_log})

def delete_food_item(request, foodname):
    foodentry = get_object_or_404(FoodItem, food_name=foodname)

    if request.method == 'POST':
        foodentry.delete()
        return redirect('food_log')

    return render(request, app_name + 'delete_fooditem.html', {'foodentry': foodentry})

# waste log

def waste_log(request):
    waste_log = WasteAudit.objects.all()
    return render(request, app_name + 'waste_log.html', {'waste_log': waste_log})

def delete_waste_audit(request, key):
    wasteaudit = get_object_or_404(WasteAudit, id=key)

    if request.method == 'POST':
        wasteaudit.delete()
        return redirect('waste_log')

    return render(request, app_name + 'delete_wasteaudit.html', {'wasteaudit': wasteaudit})



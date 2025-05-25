from django.db import models 
import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.
STATE_CHOICES = [
    ('WA', 'Western Australia'),
    ('NT', 'Northern Territory'),
    ('SA', 'South Australia'),
    ('QLD', 'Queensland'),
    ('NSW', 'New South Wales'),
    ('VIC', 'Victoria'),
    ('TAS', 'Tasmania'),
]

FOOD_CHOICES = [
    ('fruit', 'Fruit'),
    ('vegetable', 'Vegetable'),
    ('grains', 'Grains'),
    ('protein', 'Protein'),
    ('dairy', 'Dairy'),
]

WASTE_CHOICES = [
    ('expired food waste', 'Expired Food Waste'),
    ('preparation waste', 'Preparation Waste'),
    ('uneaten waste', 'Uneaten Waste'),
]

class User(AbstractUser):
    username = models.CharField(primary_key=True, max_length=40, default='default_name', unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='NT')
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    
    def __str__(self):
        return f' {self.first_name} {self.last_name}'

class FoodItem(models.Model):
    food_name = models.CharField(primary_key=True, unique=True, max_length=30)
    food_groups = models.CharField(max_length=20, choices=FOOD_CHOICES)
    bio_degradable = models.BooleanField(default=True)

    def __str__(self):
        return self.food_name

class WasteAudit(models.Model):
    entry_date = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(User(AbstractUser), on_delete=models.CASCADE)
    food_item = models.ManyToManyField(FoodItem)
    waste_type = models.CharField(max_length=20, choices=WASTE_CHOICES)
    amount = models.CharField(max_length=8, default=0)

    def __str__(self):
        return f"ID: {self.id} Entry_date: {self.entry_date}"
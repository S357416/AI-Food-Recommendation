from django.contrib import admin
from assessment4_app.models import User, FoodItem, WasteAudit

# Register your models here.
myModels = [User, FoodItem, WasteAudit]
admin.site.register(myModels)

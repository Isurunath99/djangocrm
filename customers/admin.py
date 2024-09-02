from django.contrib import admin
from .models import User,Customer,Agent,UserProfile,Category

# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Agent)
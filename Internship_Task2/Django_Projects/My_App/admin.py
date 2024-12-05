from django.contrib import admin
from .models import Department, Category, Signin, Complaint

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Signin)
admin.site.register(Complaint)

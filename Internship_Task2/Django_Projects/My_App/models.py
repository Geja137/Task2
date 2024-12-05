from django.db import models
from django.utils.timezone import now


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    

class Signin(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    Username = models.CharField(max_length=20)
    Password = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

   

class Complaint(models.Model):
    user = models.ForeignKey(Signin, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=50)
    attachment = models.FileField(upload_to="attachments/attachments", null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, default='Pending')

    
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


class Restaurant(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    dish_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    votes = models.PositiveIntegerField(default=0)
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    day_of_week = models.CharField(max_length=15, choices=DAY_CHOICES)
    date = models.DateField()

    def __str__(self):
        return self.dish_name


class Employee(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='employee_user_permissions'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='employee_groups'
    )

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class EmployeeVote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('employee', 'date')
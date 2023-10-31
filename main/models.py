from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import auth

from office import settings


# SITE
class AboutSite(models.Model):
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='media/')
    purpose = models.CharField(max_length=255)
    about = models.TextField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    gmail = models.EmailField(null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)
    location_map = models.URLField(null=True, blank=True)


class Services(models.Model):
    service_name = models.CharField(max_length=255)
    about = models.TextField()
    img = models.ImageField(upload_to='media/', null=True, blank=True)
    for_age = models.IntegerField(null=True, blank=True,)
    for_height = models.IntegerField(null=True, blank=True,)
    for_weight = models.IntegerField(null=True, blank=True,)
    for_gender = models.IntegerField(null=True, blank=True, default=1, choices=(
        (1, 'Male'),
        (2, 'Female'),
    ))

    def __str__(self):
        return self.service_name


class CalorieRequirement(models.Model):
    required_cal = models.IntegerField()

    def __int__(self):
        return self.required_cal


class Food(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField()
    img = models.ImageField(upload_to='media/')
    # in kg
    protein = models.IntegerField(null=True, blank=True)
    fats = models.IntegerField(null=True, blank=True)
    carbohydrates = models.IntegerField(null=True, blank=True)
    for_age = models.IntegerField()
    for_height = models.IntegerField()
    for_weight = models.IntegerField()
    for_gender = models.IntegerField(default=1, choices=(
        (1, 'Male'),
        (2, 'Female'),
    ))
    for_calorie = models.ForeignKey(CalorieRequirement, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Disease(models.Model):
    disease_name = models.CharField(max_length=255)
    about = models.TextField()
    img = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.disease_name


# Cabinet
class Person(AbstractUser):
    age = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    gender = models.IntegerField(default=1, choices=(
        (1, 'Male'),
        (2, 'Female'),
    ))
    symptoms = models.IntegerField(null=True, blank=True, default=1, choices=(
        (1, 'Feeling good!'),
        (2, 'Headache'),
        (3, 'Nausea'),
        (4, 'High temperature'),
        (5, 'Having cold'),
    ))
    disease = models.ForeignKey(Disease, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Patient',
        verbose_name_plural = 'Patients'


class DailyPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    plan_name = models.CharField(max_length=255)
    time = models.TimeField()
    purpose = models.CharField(max_length=255)

    def __str__(self):
        return self.plan_name


class Question(models.Model):
    from_user = models.ForeignKey(Person, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    about = models.ForeignKey(Disease, on_delete=models.CASCADE)
    message = models.TextField()


class AllowedMeal(models.Model):
    meal = models.CharField(max_length=255)

    def __str__(self):
        return self.meal


class NotAllowedMeal(models.Model):
    meal = models.CharField(max_length=255)

    def __str__(self):
        return self.meal


class PersonalDiet(models.Model):
    user = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    allowed_meals = models.ManyToManyField(AllowedMeal)
    additional = models.CharField(max_length=255)
    not_allowed = models.ManyToManyField(NotAllowedMeal)
    eat_at = models.TimeField()
    diet_for = models.ForeignKey(Disease, on_delete=models.PROTECT, null=True, blank=True)


class Notification(models.Model):
    remind = models.ForeignKey(DailyPlan, on_delete=models.CASCADE)

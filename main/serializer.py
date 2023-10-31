from rest_framework import serializers
from .models import *


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSite
        fields = '__all__'


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


class CalorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalorieRequirement
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class DailyPlanSerializer(serializers.ModelSerializer):
    product = PersonSerializer(read_only=True)

    class Meta:
        depth=2
        model = DailyPlan
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        depth=1
        model = Question
        fields = '__all__'


class PersonalDietSerializer(serializers.ModelSerializer):
    allowed_meals = serializers.PrimaryKeyRelatedField(many=True, queryset=AllowedMeal.objects.all())
    not_allowed = serializers.PrimaryKeyRelatedField(many=True, queryset=NotAllowedMeal.objects.all())

    class Meta:
        model = PersonalDiet
        fields = ['user', 'allowed_meals', 'additional', 'not_allowed', 'eat_at', 'diet_for']

    def create(self, validated_data):
        allowed_meals_data = validated_data.pop('allowed_meals')
        not_allowed_data = validated_data.pop('not_allowed')
        additional = validated_data.pop('additional')
        eat_at = validated_data.pop('eat_at')
        diet_for = validated_data.pop('diet_for')
        diet = PersonalDiet.objects.create(**validated_data)
        for meal in allowed_meals_data:
            diet.allowed_meals.add(meal)
        for meal in not_allowed_data:
            diet.not_allowed.add(meal)
        return diet

    def retrieveupdate(self, validated_data):
        allowed_meals_data = validated_data.pop('allowed_meals')
        not_allowed_data = validated_data.pop('not_allowed')
        additional = validated_data.pop('additional')
        eat_at = validated_data.pop('eat_at')
        diet_for = validated_data.pop('diet_for')
        diet = PersonalDiet.objects.create(**validated_data)
        for meal in allowed_meals_data:
            diet.allowed_meals.add(meal)
        for meal in not_allowed_data:
            diet.not_allowed.add(meal)
        return diet


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        depth=1
        model = Notification
        fields = '__all__'


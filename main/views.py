from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.decorators import login_required


@api_view(['GET'])
def home_view(request):
    site = AboutSite.objects.last()
    ser = SiteSerializer(site).data
    return Response(ser)


@api_view(['GET'])
def service_view(request):
    service = Services.objects.all()
    ser = ServicesSerializer(service, many=True).data
    return Response(ser)


@api_view(['GET'])
def calorie_view(request):
    calorie = CalorieRequirement.objects.all()
    ser = CalorieSerializer(calorie, many=True).data
    return Response(ser)


@api_view(['GET'])
def food_view(request):
    food = Food.objects.all()
    ser = FoodSerializer(food, many=True).data
    return Response(ser)


@api_view(['GET'])
def disease_view(request):
    disease = Disease.objects.all()
    ser = DiseaseSerializer(disease, many=True).data
    return Response(ser)


@permission_classes([AllowAny])
@api_view(['POST'])
def sign_up(request):
    User = get_user_model()
    if request.method == 'POST':
        username = request.data.get('username')
        age = request.data.get('age')
        height = request.data.get('height')
        weight = request.data.get('weight')
        gender = request.data.get('gender')
        symptoms = request.data.get('symptoms')
        disease = request.data.get('disease')

        new_user = User.objects.create_user(username=username, age=age, height=height, weight=weight, gender=gender, symptoms=symptoms,
                                            disease_id=disease)
        new_user.save()

        # Generate token for the new user
        refresh = RefreshToken.for_user(new_user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    return Response('Invalid request method.')


# daily plan
@api_view(['POST'])
def daily_plan(request):
    if request.method == 'POST':
        user = request.data.get('user')
        plan_name = request.data.get('plan_name')
        time = request.data.get('time')
        purpose = request.data.get('purpose')
        new_plan = DailyPlan.objects.create(user=user, plan_name=plan_name, time=time, purpose=purpose)
        new_plan.save()
        return Response('plan has been successfully submitted!')


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getuserpost(request):
    try:
        user = request.user.id
        post = DailyPlan.objects.filter(user=user).order_by('time')
        serializer = DailyPlanSerializer(post, many=True)
        return Response(serializer.data)
    except DailyPlan.DoesNotExist:
        return Response("You don't have daily plans in your list!", status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def edit_plan(request, pk):
    try:
        user = request.user.id
        post = DailyPlan.objects.filter(user=user).get(id=pk)
        plan_name = request.data.get('plan_name')
        purpose = request.data.get('purpose')
        time = request.data.get('time')
        post.plan_name = plan_name
        post.purpose = purpose
        post.time = time
        post.save()
        serializer = DailyPlanSerializer(post)
        return Response(f'The plan successfully has been updated, {serializer.data}')
    except DailyPlan.DoesNotExist:
        return Response("The plan you are trying to update does not exist.", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_plan(request, pk):
    try:
        user = request.user.id
        post = DailyPlan.objects.filter(user=user).get(id=pk)
        post.delete()
        return Response('successfully deleted')
    except DailyPlan.DoesNotExist:
        return Response("The plan you are trying to delete does not exist.", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def post_question(request):
    from_user = request.data.get('from_user')
    about = request.data.get('about')
    message = request.data.get('message')
    new_question = Question.objects.create(from_user_id=from_user, about_id=about, message=message)
    new_question.save()
    return Response('successfully created')


# visible to all
@api_view(['GET'])
@login_required
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_question(request):
    questions = Question.objects.all()
    ser = QuestionSerializer(questions, many=True).data
    return Response(ser)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_my_questions(request):
    try:
        from_user = request.user.id
        question = Question.objects.filter(from_user=from_user).all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)
    except Question.DoesNotExist:
        return Response("You don't have asked any questions!", status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def edit_question(request, pk):
    try:
        from_user = request.user.id
        question = Question.objects.filter(from_user=from_user).get(id=pk)
        about = request.data.get('about')
        message = request.data.get('message')
        question.about_id = about
        question.message = message
        question.save()
        serializer = QuestionSerializer(question)
        return Response(f'The question successfully has been updated, {serializer.data}')
    except Question.DoesNotExist:
        return Response("The question you are trying to update does not exist.", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_question(request, pk):
    try:
        from_user = request.user.id
        question = Question.objects.filter(from_user=from_user).get(id=pk)
        question.delete()
        return Response('successfully deleted')
    except Question.DoesNotExist:
        return Response("The question you are trying to delete does not exist.", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def post_diet(request):
    user = request.data.get('user')
    additional = request.data.get('additional')
    eat_at = request.data.get('eat_at')
    diet_for = request.data.get('diet_for')
    new_diet = PersonalDiet.objects.create(user_id=user, additional=additional, eat_at=eat_at, diet_for=diet_for)
    new_diet.save()
    return Response('successfully created!')


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_my_diet(request):
    try:
        user = request.user.id
        diet = PersonalDiet.objects.filter(user=user).all()
        serializer = PersonalDietSerializer(diet, many=True)
        return Response(serializer.data)
    except PersonalDiet.DoesNotExist:
        return Response("You don't have anything in diet!", status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def edit_diet(request, pk):
    try:
        user = request.user.id

        diet = PersonalDiet.objects.filter(user=user).get(id=pk)
        allowed_meals = request.data.get('allowed_meals')
        additional = request.data.get('additional')
        not_allowed = request.data.get('not_allowed')
        eat_at = request.data.get('eat_at')
        diet_for = request.data.get('diet_for')

        if allowed_meals is not None:
            diet.allowed_meals.set(allowed_meals)
        if not_allowed is not None:
            diet.not_allowed.set(not_allowed)
        diet.eat_at = eat_at
        diet.diet_for = diet_for
        diet.additional = additional
        diet.save()
        serializer = PersonalDietSerializer(diet)
        return Response(f'The diet  successfully has been updated, {serializer.data}')
    except PersonalDiet.DoesNotExist:
        return Response("The diet you are trying to update does not exist.", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_diet(request, pk):
    try:
        user = request.user.id
        diet = PersonalDiet.objects.filter(user=user).get(id=pk)
        diet.delete()
        return Response('successfully deleted')
    except PersonalDiet.DoesNotExist:
        return Response("The diet you are trying to delete does not exist on you.", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def notification_alert(request):
    try:
        plans = DailyPlan.objects.filter(user=request.user).order_by('-time')
        if plans:
            serializer = DailyPlanSerializer(plans, many=True)
            return Response(serializer.data)
        else:
            return Response("You don't have any reminders!", status=status.HTTP404NOTFOUND)
    except DailyPlan.DoesNotExist:
        return Response("Daily plan does not exist for this user!", status=status.HTTP404NOTFOUND)


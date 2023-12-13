from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate

from app.forms import LoginForm, SignUpForm, QuestionForm, SettingsForm, AnswerForm
from app.models import *

NUMBER_OF_QUESTIONS = 61

# QUESTIONS = [
#         {
#             'authorImage': 'img/avatarTemp.jpg',
#             'likesNumber': i % 10,
#             'answersNumber': i % 7 + 1,
#             'tags': ['tag' + str(i), 'tag' + str(i * i)],
#             'id': i,
#             'title': f'Question {i}',
#             'content': f'Content {i * i}',
#         } for i in range(NUMBER_OF_QUESTIONS)
#     ]
#
# ANSWERS = [
#         {
#             'id': i,
#             'authorImage': 'img/avatarTemp.jpg',
#             'likesNumber': i % 10,
#             'isCorrect': True,
#             'content': f'Content {i * i}',
#         } for i in range(NUMBER_OF_QUESTIONS)
#     ]
#
# MAIN_USER = {
#     'isAuthenticated': False,
#     'image': 'img/avatarTemp.jpg',
#     'nickName': 'obbrnu',
# }


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    try:
        newPage = paginator.page(page)
    except PageNotAnInteger:
        newPage = paginator.page(1)
    except EmptyPage:
        newPage = paginator.page(1)
    return newPage


# Create your views here.
def base(request):
    return render(request, 'base.html', )


def settings(request):
    ts = Tag.objects.amountFilter()[:7]
    return render(request, 'settings.html',{'tags': ts})


@login_required(login_url = 'login', redirect_field_name='continue')
def index(request):
    page = request.GET.get('page', 1)
    q = Question.objects.dateFilter()
    ts = Tag.objects.amountFilter()[:7]
    return render(request, 'index.html', {'items': paginate(q, page), 'tags': ts})


def hot(request):
    page = request.GET.get('page', 1)
    q = Question.objects.ratingFilter()
    ts = Tag.objects.amountFilter()[:7]
    return render(request, 'indexHot.html', {'items': paginate(q, page),'tags': ts})


def question(request, question_id):
    ts = Tag.objects.amountFilter()[:7]
    try:
        # q = Question.objects.dateFilter()[question_id - Question.objects.dateFilter()[0].id]
        q = Question.objects.all()[question_id - 1]
        a = q.answers.all()
        page = request.GET.get('page', 1)
        print(request.GET)
        print(request.POST)
        if request.method == "GET":
            answer_form = AnswerForm()
        if request.method == "POST":
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                text = answer_form.cleaned_data['text']
                author = Profile.objects.get(id=request.user.id)
                date = datetime.datetime(2023, 1, 1)
                ans = Answer(relatedQuestion=q, text=text, author=author, date=date, rating=0, correct=False)
                ans.save()
            answer_form.clean()
    except:
        return HttpResponse(status=404)
    return render(request, 'question.html', {'question': q, 'items': paginate(a, page), 'form': answer_form, 'tags': ts})


def tag(request, s: str):
    ts = Tag.objects.amountFilter()[:7]
    try:
        t = Tag.objects.get(text=s)
    except:
        return HttpResponse(status=404)
    q = Question.objects.tagFilter(t)
    page = request.GET.get('page', 1)
    return render(request, 'tag.html', {'tag': t, 'items': paginate(q, page), 'tags': ts})


def ask(request):
    ts = Tag.objects.amountFilter()[:7]
    if request.method == "GET":
        question_form = QuestionForm()
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            title = question_form.cleaned_data['title']
            text = question_form.cleaned_data['text']
            ttags = question_form.cleaned_data['tags']
            author = Profile.objects.get(id=request.user.id)
            date = datetime.datetime(2023, 1, 1)
            rating = 0
            q = Question(title=title, text=text, author=author, date=date, rating=rating)
            q.save()
            for tag in ttags:
                t = Tag.objects.get(id=tag.id)

                t.amount += 1
                t.save()
                q.tags.add(t)
                q.save()
            if q:
                print("Succesfully ask")
                return redirect(f'/question/{q.id}')
    return render(request, "ask.html", {"form": question_form, 'tags': ts})


def log_in(request):
    ts = Tag.objects.amountFilter()[:7]
    print(request.GET)
    print(request.POST)
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            print(user)
            if user is not None:
                login(request, user)
                print("Succesfully logged in")
                return redirect(reverse('index'))
    return render(request, 'login.html', context={"form": login_form,'tags': ts})


def log_out(request):
    auth.logout(request)
    return redirect(reverse('login'))


def signup(request):
    ts = Tag.objects.amountFilter()[:7]
    print(request.GET)
    print(request.POST)
    if request.method == "GET":
        reg_form = SignUpForm()
    if request.method == "POST":
        reg_form = SignUpForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            # user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                p = Profile(user=user, avatar='img/avatarTemp.jpg')
                p.save()
                print("Succesfully reg")
                return redirect(reverse("index"))
    return render(request, "signup.html", {"form": reg_form,'tags': ts})

@login_required()
def settings(request):
    ts = Tag.objects.amountFilter()[:7]
    if request.method == "GET":
        user_form = SettingsForm(initial={"username": request.user.username, "email": request.user.email})
    if request.method == "POST":
        user_form = SettingsForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password0 = user_form.cleaned_data['password0']
            password = user_form.cleaned_data['password']
            email = user_form.cleaned_data['email']
            user1 = authenticate(username=request.user.username, password=password0)
            if user1:
                user = request.user
                user.username = username
                if len(password) > 0:
                    user.set_password(password)
                user.email = email
                user.save()
    return render(request, "settings.html", {"form": user_form,'tags': ts})
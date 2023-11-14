from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
MAIN_USER = {
    'isAuthenticated': False,
    'image': 'img/avatarTemp.jpg',
    'nickName': 'obbrnu',
    }


def paginate(objects, page, per_page=20):
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
    return render(request, 'base.html')


def index(request):
    page = request.GET.get('page', 1)
    q = Question.objects.dateFilter()
    return render(request,'index.html', {'items': paginate(q, page), 'mainUser': MAIN_USER})


def hot(request):
    page = request.GET.get('page', 1)
    q = Question.objects.ratingFilter()
    return render(request,'indexHot.html', {'items': paginate(q, page), 'mainUser': MAIN_USER})


def question(request, question_id):
    try:
        # q = Question.objects.dateFilter()[question_id - Question.objects.dateFilter()[0].id]
        q = Question.objects.all()[question_id - 1]
    except:
        return HttpResponse(status = 404)
    a = q.answers.all()
    page = request.GET.get('page', 1)
    return render(request,'question.html', {'question': q, 'items': paginate(a, page)})


def tag(request, s: str):
    try:
        t = Tag.objects.get(text = s)
    except:
        return HttpResponse(status = 404)
    q = Question.objects.tagFilter(t)
    page = request.GET.get('page', 1)
    return render(request, 'tag.html', {'tag': t, 'items': paginate(q, page)})


def ask(request):
    return render(request,'ask.html')


def login(request):
    return render(request,'login.html')


def signup(request):
    return render(request,'signup.html')
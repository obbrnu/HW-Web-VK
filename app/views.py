from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

NUMBER_OF_QUESTIONS = 61

QUESTIONS = [
        {
            'authorImage': 'img/avatarTemp.jpg',
            'likesNumber': i % 10,
            'answersNumber': i % 7 + 1,
            'tags': ['tag' + str(i), 'tag' + str(i * i)],
            'id': i,
            'title': f'Question {i}',
            'content': f'Content {i * i}',
        } for i in range(NUMBER_OF_QUESTIONS)
    ]

ANSWERS = [
        {
            'id': i,
            'authorImage': 'img/avatarTemp.jpg',
            'likesNumber': i % 10,
            'isCorrect': True,
            'content': f'Content {i * i}',
        } for i in range(NUMBER_OF_QUESTIONS)
    ]

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
    return render(request,'index.html', {'items': paginate(QUESTIONS, page), 'mainUser': MAIN_USER})


def question(request, question_id):
    item = QUESTIONS[question_id]
    page = request.GET.get('page', 1)
    return render(request,'question.html', {'question': item, 'items': paginate(ANSWERS, page)})


def ask(request):
    return render(request,'ask.html')


def login(request):
    return render(request,'login.html')


def signup(request):
    return render(request,'signup.html')
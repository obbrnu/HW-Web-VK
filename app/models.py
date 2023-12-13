from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    avatar = models.ImageField(default='img/avatarTemp.jpg')
    def __str__(self):
        return f"{self.user.username}"


class TagManager(models.Manager):
    def amountFilter(self):
        return self.order_by('-amount')


class Tag(models.Model):
    text = models.CharField(max_length=20, default="all", unique=True)
    amount = models.IntegerField(default=0)

    objects = TagManager()

    def __str__(self) -> str:
        return f"{self.text}"


class QuestionManager(models.Manager):
    def tagFilter(self, specialTag):
        return self.filter(tags=specialTag)

    def dateFilter(self):
        return self.order_by('-date')

    def ratingFilter(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(Profile, models.CASCADE, related_name='questions')
    date = models.DateField(default=datetime.datetime(2023, 1, 1))
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def ratingUp(self):
        self.rating += 1
        self.save()

    def ratingDown(self):
        self.rating -= 1
        self.save()

    def getTags(self):
        return self.tags


class AnswerManager(models.Manager):
    def rateFilter(self):
        return self.order_by('-rating')

    def dateFilter(self):
        return self.order_by('-date')


class Answer(models.Model):
    relatedQuestion = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(Profile, models.CASCADE, related_name='answers')
    date = models.DateField(default=datetime.datetime(2023, 1, 1))
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self) -> str:
        return self.text

    def ratingUp(self):
        self.rating += 1
        self.save()

    def ratingDown(self):
        self.rating -= 1
        self.save()


class QuestionLike(models.Model):
    relatedQuestion = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, models.CASCADE)
    like = models.BooleanField(blank=True, default=False)

    def __str__(self) -> str:
        return f'{self.user.user.username} likes question {self.like}'


class AnswerLike(models.Model):
    relatedAnswer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, models.CASCADE)
    like = models.BooleanField(blank=True, default=False)

    def __str__(self) -> str:
        return f'{self.user.user.username} likes answer {self.like}'
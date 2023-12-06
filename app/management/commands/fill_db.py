from django.core.management import BaseCommand
from faker import Faker
from app.models import User, Profile, Tag, Question, Answer, AnswerLike, QuestionLike
import random
from random import randint

fake = Faker()

class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        numberOfUsers = ratio
        numberOfQuestions = ratio * 10
        numberOfAnswers = ratio * 100
        numberOfTags = ratio
        numberOfQuestionLikes = ratio * 100
        numberOfAnswerLikes = ratio * 100
        userList = []
        profileList = []
        for i in range(numberOfUsers):
            userTmp = User(username =str(i) + ' ' + fake.first_name(),
                           password = 'FirstPass1')
            profileTmp = Profile(user = userTmp)
            userList.append(userTmp)
            profileList.append(profileTmp)
        User.objects.bulk_create(userList)
        Profile.objects.bulk_create(profileList)

        tagList = [
            Tag(
                text=str(i) + 'tags' + fake.text(max_nb_chars=5)
            ) for i in range(numberOfTags)
        ]
        Tag.objects.bulk_create(tagList)

        for i in range(numberOfQuestions):
            profile = Profile.objects.get(id=Profile.objects.first().id + randint(0, numberOfUsers - 1))
            question = Question(title=fake.text(max_nb_chars = 10 + i % 15),
                                text=fake.text(max_nb_chars = 20 + i % 50),
                                author=profile,
                                date=fake.date(),
                                rating = 0)
            question.save()
            tag = Tag.objects.get(id=Tag.objects.first().id + randint(1, numberOfTags - 1))
            question.tags.add(tag)
            question.save()

            for j in range(10):
                profile = Profile.objects.get(id=Profile.objects.first().id + randint(0, numberOfUsers - 1))
                a = Answer(relatedQuestion = question,
                           text=fake.text(max_nb_chars = 20 + i % 50),
                           author=profile,
                           date=fake.date(),
                           rating=0,
                           correct=False)
                a.save()

        for i in range(numberOfQuestionLikes):
            question = Question.objects.get(id=Question.objects.first().id + randint(0, numberOfQuestions - 1))
            profile = Profile.objects.get(id=Profile.objects.first().id + randint(0, numberOfUsers - 1))
            like = random.choice([True, False])
            questionLike = QuestionLike(relatedQuestion=question,
                                        user=profile,
                                        like=like)
            questionLike.save()
            answer = Answer.objects.get(id=Answer.objects.first().id + randint(0, numberOfAnswers - 1))
            profile = Profile.objects.get(id=Profile.objects.first().id + randint(0, numberOfUsers - 1))
            like = random.choice([True, False])
            answerLike = AnswerLike(relatedAnswer=answer,
                                    user=profile,
                                    like=like)
            answerLike.save()
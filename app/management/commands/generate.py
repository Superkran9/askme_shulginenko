from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import (
    Profile,
    Tag,
    Question,
    Answer,
    LikeQ,
    LikeA
)
import random


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
        parser.add_argument('offset', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        offset = options['offset']
        self.profiles_gen(ratio, offset)
        profiles = Profile.objects.all()
        self.tags_gen(ratio, offset)
        tags = Tag.objects.all()
        self.questions_gen(profiles, ratio, offset)
        questions = Question.objects.all()
        self.answers_gen(profiles, questions, ratio, offset)
        answers = Answer.objects.all()
        self.q_likes_gen(profiles, questions, ratio)
        self.a_likes_gen(profiles, answers, ratio)
        for question in questions:
            tags_to_add = random.choices(tags, k=3)
            for t in tags_to_add:
                question.tags.add(t)

    def profiles_gen(self, ratio, offset):
        self.stdout.write("profile generating...\n")

        def user_gen(number):
            user_d = {
                'username': f'#{number}User',
                'first_name': f'Bot#{number}',
                'last_name': f'Afk{number}',
                'password': 'q1w2e3r4t5y6',
                'email': f'bot{number}@example.com',
                'is_staff': False,
                'is_active': True,
                'is_superuser': False
            }
            return user_d

        profiles = []
        for i in range(ratio):
            if i % 1000 == 0:
                print(f'{i} profiles gererated\n')
            user = User.objects.create_user(**user_gen(i + offset))
            profile = Profile(user=user)
            profiles.append(profile)

        Profile.objects.bulk_create(profiles)

    def tags_gen(self, count, offset):
        self.stdout.write("tags generating...\n")
        tags = []

        for i in range(count):
            if i % 1000 == 0:
                print(f'{i} tags gererated\n')
            tag = Tag(title=f'tag#{i + offset}')
            tags.append(tag)
        Tag.objects.bulk_create(tags)

    def questions_gen(self, profiles, ratio, offset):
        self.stdout.write("questions generating...\n")
        questions = []
        for i in range(10 * ratio):
            if i % 10000 == 0:
                print(f'{i} questions gererated\n')
            author = random.choice(profiles)
            question = Question()
            question.title = f'Question#{i + 10 * offset}'
            question.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            question.author = author
            questions.append(question)
        Question.objects.bulk_create(questions)

    def answers_gen(self, profiles, questions, ratio, offset):
        self.stdout.write("answers generating...\n")
        answers = []
        for i in range(100 * ratio):
            if i % 100000 == 0:
                print(f'{i} answers gererated\n')
            answer = Answer(author=random.choice(profiles),
                            question=random.choice(questions),
                            text=f'Answer#{i}')

            answers.append(answer)
            if i%500000 == 0:
                Answer.objects.bulk_create(answers)
                answers.clear()
        Answer.objects.bulk_create(answers)

    def q_likes_gen(self, profiles, questions, ratio):
        self.stdout.write("question likes generating...\n")
        likes = []
        current_likes = []
        for i in range(150 * ratio):
            if i % 150*1000 == 0:
                print(f'{i} question likes gererated\n')
            like = LikeQ(user=random.choice(profiles), question=random.choice(questions))
            while like in likes:
                like = LikeQ(user=random.choice(profiles), question=random.choice(questions))
            current_likes.append(like)
            likes.append(like)

        LikeQ.objects.bulk_create(current_likes)

    def a_likes_gen(self, profiles, answers, ratio):
        self.stdout.write("answer likes generating...\n")
        likes = []
        current_likes = []
        for i in range(50 * ratio):
            if i % 50*1000 == 0:
                print(f'{i} answer likes gererated\n')
            like = LikeA(user=random.choice(profiles), answer=random.choice(answers))
            while like in likes:
                like = LikeA(user=random.choice(profiles), answer=random.choice(answers))
            likes.append(like)
            current_likes.append(like)
        LikeA.objects.bulk_create(current_likes)
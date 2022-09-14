from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Status(models.IntegerChoices):
    DELETED = 0, 'Deleted'
    ACTIVE = 1, 'Active'


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.ACTIVE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Difficulty(models.IntegerChoices):
    EASY = 0, 'Easy'
    MODERATE = 1, 'Moderate'
    COMPLEX = 2, 'Complex'


class Gender(models.IntegerChoices):
    EVERYTHING = 0, 'Everything'
    MALE = 1, 'Male'
    FEMALE = 2, 'Female'


class Tag(BaseModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    linked = models.BooleanField(default=False)
    objects = models.Manager()


class Word(BaseModel):
    # questions = models.ManyToManyField(Question)
    word = models.CharField(max_length=30, blank=False, null=False)
    # linked = models.BooleanField(default=False)
    objects = models.Manager()


class Question(BaseModel):
    id = models.IntegerField(primary_key=True)
    question = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag)
    rate = models.PositiveSmallIntegerField(default=5)
    difficulty = models.PositiveSmallIntegerField(
        choices=Difficulty.choices,
        default=Difficulty.EASY
    )
    image_url = models.ImageField(
        upload_to='questions_data/images', null=True, blank=True)
    # color_stuff = models.CharField(max_length=140, blank=False, default='') Tabla aparte?
    words = models.ManyToManyField(Word)
    objects = models.Manager()

class ImageActivity(BaseModel):
    id = models.IntegerField(primary_key=True)
    image_url = models.ImageField(
        upload_to='questions_data/images', null=True, blank=True)
    objects = models.Manager()


class UserSentence(BaseModel):
    sentence = models.CharField(max_length=20, blank=False, null=False)
    meaning = models.CharField(max_length=20, blank=True, default='')
    total_uses = models.PositiveSmallIntegerField(default=0)
    last_time_used = models.DateTimeField()
    # Posiblemente agregar palabra dificil, palabra que quiero repetirla mas seguido
    known = models.BooleanField(default=False)
    objects = models.Manager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class UserQuestion(BaseModel):
    total_uses = models.PositiveSmallIntegerField(default=0)
    last_time_used = models.DateTimeField()
    objects = models.Manager()

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class UserScreenFlow(BaseModel):
    type = models.CharField(max_length=140, blank=False, null=False)
    objects = models.Manager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class UserProfile(BaseModel):
    total_words = models.PositiveSmallIntegerField(default=0)
    verified = models.BooleanField(default=False)
    objects = models.Manager()

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

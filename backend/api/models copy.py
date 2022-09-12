from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Status(models.IntegerChoices):
    ACTIVE = 0, 'Active'
    DELETED = 1, 'Deleted'


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
    LOW = 0, 'Low'
    NORMAL = 1, 'Normal'
    HIGH = 2, 'High'


class Gender(models.IntegerChoices):
    EVERYTHING = 0, 'Everything'
    MALE = 1, 'Male'
    FEMALE = 2, 'Female'


class Tag(BaseModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    linked = models.BooleanField(default=False)
    objects = models.Manager()


class Question(BaseModel):
    question = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag)
    rate = models.PositiveSmallIntegerField(default=5)
    index = models.PositiveSmallIntegerField(default=0)
    parent_id = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True)
    linked = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='questions_data/images', null=True, blank=True)
    # color_stuff = models.CharField(max_length=140, blank=False, default='') Tabla aparte?
    objects = models.Manager()


class WordType(models.IntegerChoices):
    VERB = 0, 'Verb'
    ADJ = 1, 'Adj'
    ADJC = 2, 'Adj comparative'
    ADJS = 3, 'Adj superlative'
    NOUN = 4, 'Noun singular'
    NOUNS = 5, 'Noun plural'


class LinkedWord(BaseModel):
    type = models.PositiveSmallIntegerField(
        null=False, blank=False, choices=WordType.choices)
    questions = models.ManyToManyField(Question)
    word = models.CharField(max_length=30, blank=False, null=False)
    linked = models.BooleanField(default=False)
    objects = models.Manager()


class UserWord(BaseModel):
    sentence = models.CharField(max_length=30, blank=False, null=False)
    meaning = models.CharField(max_length=100, blank=True, default='')
    total_uses = models.PositiveSmallIntegerField(default=0)
    last_use = models.DateTimeField()
    # Posiblemente agregar palabra dificil, palabra que quiero repetirla mas seguido
    known = models.BooleanField(default=False)
    objects = models.Manager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class UserQuestion(BaseModel):
    total_uses = models.PositiveSmallIntegerField(default=0)
    last_use = models.DateTimeField()
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

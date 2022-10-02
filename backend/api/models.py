from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Status(models.IntegerChoices):
    DELETED = 0, 'Deleted'
    ACTIVE = 1, 'Active'


class Difficulty(models.IntegerChoices):
    EASY = 0, 'Easy'
    MODERATE = 1, 'Moderate'
    COMPLEX = 2, 'Complex'


class ActivityTypes(models.IntegerChoices):
    QUESTION = 0, 'Question'
    DESCRIBE_IMAGE = 1, 'Describe Image'


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


class Tag(BaseModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    linked = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        db_table = 'tags'


class Word(BaseModel):
    word = models.CharField(max_length=30, blank=False, null=False)
    objects = models.Manager()

    class Meta:
        db_table = 'words'


class QuestionActivity(BaseModel):
    id = models.IntegerField(primary_key=True)
    question = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag)
    rate = models.PositiveSmallIntegerField(default=5)
    difficulty = models.PositiveSmallIntegerField(
        choices=Difficulty.choices,
        default=Difficulty.EASY
    )
    image_url = models.TextField(null=False, blank=False)
    voice_url = models.TextField(null=False, blank=False)
    words = models.ManyToManyField(Word)
    objects = models.Manager()

    class Meta:
        db_table = 'question_activities'


class DescribeImageActivity(BaseModel):
    id = models.IntegerField(primary_key=True)
    image_url = models.TextField(null=False, blank=False)
    objects = models.Manager()

    class Meta:
        db_table = 'describeimage_activities'


class Example(BaseModel):
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=ActivityTypes.choices
    )
    example = models.JSONField(null=False, blank=False)
    voice_url = models.TextField(null=False, blank=False)
    activity_id = models.IntegerField(null=True, blank=True)
    word_text = models.CharField(max_length=30, null=True, blank=True)
    objects = models.Manager()

    class Meta:
        db_table = 'examples'


class Style(BaseModel):
    background_word = models.CharField(max_length=20, blank=True, null=True)
    background_screen = models.CharField(
        max_length=20, blank=False, null=False)
    activity_id = models.IntegerField(null=False)
    type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=ActivityTypes.choices
    )
    objects = models.Manager()

    class Meta:
        db_table = 'styles'


class UserSentence(BaseModel):
    sentence = models.CharField(max_length=20, blank=False, null=False)
    meaning = models.CharField(max_length=100, blank=True, default='')
    total_uses = models.PositiveSmallIntegerField(default=0)
    last_time_used = models.DateTimeField(null=True)
    # Posiblemente agregar palabra dificil, palabra que quiero repetirla mas seguido
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    objects = models.Manager()

    class Meta:
        db_table = 'user_sentences'


class UserActivityHistory(BaseModel):
    total_uses = models.PositiveSmallIntegerField(default=0)
    last_time_used = models.DateTimeField()
    activity_id = models.IntegerField(null=False)
    type = models.PositiveSmallIntegerField(
        null=False,
        choices=ActivityTypes.choices
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    objects = models.Manager()

    class Meta:
        db_table = 'user_activity_history'


class UserScreenFlow(BaseModel):
    type = models.CharField(max_length=150, blank=False, null=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    objects = models.Manager()

    class Meta:
        db_table = 'user_screenflow'


class UserProfile(BaseModel):
    total_words = models.PositiveSmallIntegerField(default=0)
    verified = models.BooleanField(default=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    objects = models.Manager()

    class Meta:
        db_table = 'user_profiles'

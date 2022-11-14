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


class QuestionTypes(models.IntegerChoices):
    NORMAL = 0, 'Normal'
    DESCRIBE_IMAGE = 1, 'Describe image'
    TEACHER = 2, 'Teacher'


class WordTypes(models.IntegerChoices):
    NORMAL = 0, 'Normal'
    GROUP = 1, 'Group'


class WordOrigin(models.IntegerChoices):
    RANDOM = 0, 'Random generated'
    SAVED = 1, 'Saved from library'
    USER = 2, 'Created by user'


class SourceTypes(models.IntegerChoices):
    SHORT_VIDEO = 0, 'Short video'
    INFO_CARD = 1, 'Info card'


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


class Question(BaseModel):
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
        db_table = 'questions'


class ShortVideo(BaseModel):
    id = models.IntegerField(primary_key=True)
    cover = models.TextField(null=False, blank=False)
    url = models.TextField(null=False, blank=False)
    objects = models.Manager()

    class Meta:
        db_table = 'short_videos'


class InfoCard(BaseModel):
    id = models.IntegerField(primary_key=True)
    image_url = models.TextField(null=False, blank=False)
    voice_url = models.TextField(null=False, blank=False)
    objects = models.Manager()

    class Meta:
        db_table = 'info_cards'


class Collocation(BaseModel):
    text = models.CharField(max_length=150, null=True, blank=True)
    source_type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=SourceTypes.choices
    )
    short_video = models.ForeignKey(
        ShortVideo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    info_card = models.ForeignKey(
        InfoCard,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    objects = models.Manager()

    class Meta:
        db_table = 'collocations'


class Example(BaseModel):
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=ActivityTypes.choices
    )
    example = models.JSONField(null=False, blank=False)
    voice_url = models.TextField(null=False, blank=False)
    word_text = models.CharField(max_length=30, null=True, blank=True)
    objects = models.Manager()
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'examples'


class Style(BaseModel):
    background_screen = models.CharField(
        max_length=20, blank=False, null=False)
    background_challenge = models.CharField(
        max_length=20, blank=True, null=True)
    use_gradient = models.BooleanField(default=False)
    bottom_gradient_color = models.CharField(
        max_length=20, blank=True, null=True)
    top_gradient_color = models.CharField(max_length=20, blank=True, null=True)
    question_position = models.DecimalField(
        default=0.3, max_digits=3, decimal_places=2)
    image_position = models.DecimalField(
        default=0.1, max_digits=3, decimal_places=2)
    question_font_size = models.DecimalField(
        default=21.0, max_digits=3, decimal_places=1)
    question_opacity = models.DecimalField(
        default=0.4, max_digits=3, decimal_places=2)
    objects = models.Manager()
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'styles'


class Sentence(BaseModel):
    sentence = models.CharField(max_length=20, blank=False, null=False)
    meaning = models.CharField(max_length=100, blank=True, default='')
    extras = models.TextField(blank=True, default='')
    type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=WordTypes.choices
    )
    source_type = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=SourceTypes.choices
    )
    short_video = models.ForeignKey(
        ShortVideo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    info_card = models.ForeignKey(
        InfoCard,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    objects = models.Manager()

    class Meta:
        db_table = 'sentences'


class UserSentence(BaseModel):
    sentence = models.CharField(max_length=20, blank=False, null=False)
    meaning = models.CharField(max_length=100, blank=True, default='')
    extras = models.TextField(blank=True, default='')
    total_uses = models.PositiveSmallIntegerField(default=0)
    last_time_used = models.DateTimeField(null=True)
    type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=WordTypes.choices
    )
    origin = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=WordOrigin.choices
    )
    source_type = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=SourceTypes.choices
    )
    short_video = models.ForeignKey(
        ShortVideo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    info_card = models.ForeignKey(
        InfoCard,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
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
    activity_id = models.IntegerField(null=False, blank=False)
    type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=ActivityTypes.choices
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    objects = models.Manager()

    class Meta:
        db_table = 'user_history'


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

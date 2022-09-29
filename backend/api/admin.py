from django.contrib import admin
from api.models import (
    Tag, 
    QuestionActivity, Word
)

# Register your models here.
admin.site.register(Tag)
# admin.site.register(Category)
admin.site.register(QuestionActivity)
admin.site.register(Word)

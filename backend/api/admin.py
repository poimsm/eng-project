from django.contrib import admin
from api.models import (
    Tag, 
    Question, Word
)

# Register your models here.
admin.site.register(Tag)
# admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Word)

from django.contrib import admin
from api.models import (
    Tag, 
    Question, LinkedWord
)

# Register your models here.
admin.site.register(Tag)
# admin.site.register(Category)
admin.site.register(Question)
admin.site.register(LinkedWord)

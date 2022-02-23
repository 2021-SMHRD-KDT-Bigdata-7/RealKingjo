from django.contrib import admin

from .models import life_Question
# Register your models here.

class life_QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
admin.site.register(life_Question, life_QuestionAdmin)
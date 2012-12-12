from django.contrib import admin
from red_cross_project.clean_bbs.models import Question

class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)
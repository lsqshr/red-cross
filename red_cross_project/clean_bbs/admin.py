from django.contrib import admin
from red_cross_project.clean_bbs.models import Question,TempProfile

class QuestionAdmin(admin.ModelAdmin):
    pass

class TempProfileAdmin(admin.ModelAdmin):
	pass

admin.site.register(Question, QuestionAdmin)
admin.site.register(TempProfile, TempProfileAdmin)
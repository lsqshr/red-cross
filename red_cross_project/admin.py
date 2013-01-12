from django.contrib import admin
from red_cross_project.models import ExtraProfile

class ExtraProfileAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(ExtraProfile, ExtraProfileAdmin)
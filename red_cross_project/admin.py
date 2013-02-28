from django.contrib import admin
from red_cross_project.models import ExtraProfile, Staff, Field

class ExtraProfileAdmin(admin.ModelAdmin):
	pass

class StaffAdmin(admin.ModelAdmin):
	pass

class FieldAdmin(admin.ModelAdmin):
	pass

admin.site.register(ExtraProfile, ExtraProfileAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Field, FieldAdmin)
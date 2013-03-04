from django.contrib import admin
from red_cross_project.clean_post.models import Post,Reply 

class PostAdmin(admin.ModelAdmin):
    pass

class ReplyAdmin(admin.ModelAdmin):
	pass

admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
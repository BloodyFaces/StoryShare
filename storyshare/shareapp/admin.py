from django.contrib import admin
from .models import Story, ProfileInfo, Comment, Appraisal

class StoryAdmin(admin.ModelAdmin):

	list_display = ["topic", "content", "draft", "user", "created"]
	class Meta:
		model = Story


class CommentAdmin(admin.ModelAdmin):
	list_display = ["user", "story", "published", "content"]

	class Meta:
		model = Comment


class AppraisalAdmin(admin.ModelAdmin):

	list_display = ["user", "positive", "story"]

	class Meta:
		model = Appraisal
		

admin.site.register(Story, StoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Appraisal, AppraisalAdmin)
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_userforeignkey.models.fields import UserForeignKey


def get_sentinel_user():
	return get_user_model().objects.get_or_create(username='deleted')[0]


def upload_location(instance, filename):
	return "%s/%s" % (instance.id, filename)


class Story(models.Model):

	class Meta:
		verbose_name_plural = "Stories"

	topic = models.CharField(max_length=64, null=False, blank=False)
	content = models.TextField(null=False, blank=False)
	user = UserForeignKey(auto_user_add=True, on_delete=models.CASCADE)
	draft = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	published = models.DateTimeField(auto_now=True, auto_now_add=False)

	def get_absolute_url(self):
		return reverse("update-story", kwargs={"pk": self.id})

	def __str__(self):
		return self.user.username


class Comment(models.Model):
	content = models.TextField(null=False, blank=False)
	story = models.ForeignKey(Story, on_delete=models.CASCADE)
	user = UserForeignKey(auto_user_add=True, on_delete=models.CASCADE)
	published = models.DateTimeField(auto_now=False, auto_now_add=True)


class Appraisal(models.Model):
	positive = models.BooleanField(default=True)
	story = models.ForeignKey(Story, on_delete=models.CASCADE)
	user = UserForeignKey(auto_user_add=True, on_delete=models.CASCADE)


class ProfileInfo(models.Model):
	image = models.ImageField(null=True, blank=True, upload_to=upload_location)
	banned = models.BooleanField(default=False)
	user = UserForeignKey(auto_user_add=True, on_delete=models.CASCADE)

	def getImage(self):
		img = self.image
		if not img:
			img = ProfileInfo.objects.get(pk=1).image
		return img

	def __str__(self):
		return self.user.username
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import (
	CreateView,
	DetailView,
	ListView,
	UpdateView,
	ListView,
	DeleteView,
	FormView
)

from .models import Story, ProfileInfo, Appraisal, Comment
from .forms import StoryForm, ProfileForm, CommentForm


class HomeTopListView(ListView):
	model = Story
	template_name = 'home.html'

	def get_queryset(self):
		stories = Story.objects.annotate(Count('appraisal')).filter(draft=False).order_by('-appraisal__count')[:5]
		for story in stories:
			story.image = story.user.profileinfo_set.all()[0].getImage().url
			story.author = story.user.username
			story.firstname = story.user.first_name
			story.lastname = story.user.last_name
			story.likes = len(Appraisal.objects.filter(story=story, positive=True))
			story.dislikes = len(Appraisal.objects.filter(story=story, positive=False))
		return stories


class AllStoriesListView(ListView):
	model = Story
	template_name = "all_story.html"

	def get_queryset(self):
		stories = Story.objects.filter(draft=False).order_by("-published")
		for story in stories:
			story.image = story.user.profileinfo_set.all()[0].getImage().url
			story.author = story.user.username
			story.firstname = story.user.first_name
			story.lastname = story.user.last_name
			story.likes = len(Appraisal.objects.filter(story=story, positive=True))
			story.dislikes = len(Appraisal.objects.filter(story=story, positive=False))
		return stories


class StoryDetailView(View):

	template_name = 'story_detail.html'

	def get(self, request, *args, **kwargs):
		obj = get_object_or_404(Story, pk=self.kwargs.get("pk"))
		try:
			obj.liked = Appraisal.objects.get(story=obj, user=self.request.user, positive=True)
		except Appraisal.DoesNotExist:
			print("User hasn't liked")
		try:
			obj.disliked = Appraisal.objects.get(story=obj, user=self.request.user, positive=False)
		except Appraisal.DoesNotExist:
			print("User hasn't disliked")
		comments = Comment.objects.filter(story=obj).order_by("-published")
		for comment in comments:
			comment.image = comment.user.profileinfo_set.all()[0].getImage().url
			comment.author = comment.user.username
			comment.firstname = comment.user.first_name
			comment.lastname = comment.user.last_name
		form = CommentForm()
		context = {
			"object": obj,
			"comments": comments,
			"form": form
		}
		return render(request, self.template_name, context)


	def post(self, request, *args, **kwargs):
		form = CommentForm(request.POST)
		if form.is_valid():
			story = get_object_or_404(Story, pk=kwargs["pk"])
			new_comment = Comment(user=request.user, story=story, content=form.instance.content)
			new_comment.save()
		obj = get_object_or_404(Story, pk=self.kwargs.get("pk"))
		try:
			obj.liked = Appraisal.objects.get(story=obj, user=self.request.user, positive=True)
		except Appraisal.DoesNotExist:
			print("User hasn't liked")
		try:
			obj.disliked = Appraisal.objects.get(story=obj, user=self.request.user, positive=False)
		except Appraisal.DoesNotExist:
			print("User hasn't disliked")
		comments = Comment.objects.filter(story=obj).order_by("-published")
		print(comments)
		for comment in comments:
			comment.image = comment.user.profileinfo_set.all()[0].getImage().url
			comment.author = comment.user.username
			comment.firstname = comment.user.first_name
			comment.lastname = comment.user.last_name
		form = CommentForm()
		context = {
			"object": obj,
			"comments": comments,
			"form": form
		}
		return render(request, self.template_name, context)


class StoryCreateView(CreateView):
	model = Story
	template_name = 'story_update.html'
	form_class = StoryForm

	def form_valid(self, form):
		if "publish" in self.request.POST:
			form.instance.draft = False
		return super().form_valid(form)

	def clean_user(self):
		return self.request.user

	def get_success_url(self):
		return reverse("user-profile")


class StoryUpdateView(UpdateView):
	model = Story
	template_name = 'story_update.html'
	form_class = StoryForm


	def form_valid(self, form):
		if "publish" in self.request.POST:
			form.instance.draft = False
		return super().form_valid(form)

	def get_object(self):
		return get_object_or_404(Story, pk=self.kwargs.get("pk"))


	def get_success_url(self):
		return reverse("home-top-list")


class StoryDeleteView(DeleteView):
	model = Story

	def get_object(self):
		return get_object_or_404(Story, pk=self.kwargs.get("pk"))

	def get_success_url(self):
		return reverse("user-profile")


class ProfileView(View):
	template_name = "user_profile.html"

	def get(self, request, *args, **kwargs):
		user_stories = Story.objects.filter(user=request.user).order_by("-published")
		profile = ProfileInfo.objects.get_or_create(user=request.user)[0]
		profile.imageUrl = profile.getImage().url
		profile.storyCount = len(user_stories)
		rating = Appraisal.objects.filter(story__in=user_stories)
		profile.rating = len(rating)
		profile.likes = len(rating.filter(positive=True))
		profile.dislikes = len(rating.filter(positive=False))
		context = {
			"user_stories": user_stories,
			"profile": profile
		}
		return render(request, self.template_name, context)


class ProfileEditView(View):
	template_name = "profile_edit.html"

	def get(self, request, *args, **kwargs):
		profile = ProfileInfo.objects.get(user=request.user)
		form = ProfileForm(instance=profile, initial={"name": request.user.first_name, "surname": request.user.last_name})
		context = {
			"form": form
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			user = get_object_or_404(User, id=request.user.id)
			user.first_name = form.cleaned_data['name']
			user.last_name = form.cleaned_data['surname']
			user.save()
			prof = get_object_or_404(ProfileInfo, user=request.user)
			if form.instance.image:
				prof.image = form.instance.image
			prof.save()
		context = {
			"form": form
		}
		return render(request, self.template_name, context)


@login_required(login_url='/accounts/login/')
def add_like(request):
	story_id = request.GET.get('story_id')
	story = Story.objects.get(id=story_id)
	appraisal = Appraisal(story=story, user=request.user, positive=True)
	appraisal.save()
	data = {
        'success': True
    }
	return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def add_dislike(request):
	story_id = request.GET.get('story_id')
	story = Story.objects.get(id=story_id)
	appraisal = Appraisal(story=story, user=request.user, positive=False)
	appraisal.save()
	data = {
        'success': True
    }
	return JsonResponse(data)
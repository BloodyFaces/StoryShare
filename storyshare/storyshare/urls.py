"""storyshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from shareapp.views import (
    HomeTopListView, 
    StoryDetailView, 
    StoryCreateView, 
    StoryUpdateView, 
    StoryDeleteView, 
    ProfileView,
    AllStoriesListView,
    ProfileEditView,
    add_like,
    add_dislike
)

urlpatterns = [
	path('', HomeTopListView.as_view(), name="home-top-list"),
    path('admin/', admin.site.urls),
    path('create/', login_required(StoryCreateView.as_view()), name='create-story'),
    path('add_like/', add_like, name='add-like'),
    path('add_dislike/', add_dislike, name='add-dislike'),
    path('<int:pk>/', login_required(StoryDetailView.as_view()), name="detail-story"),
    path('<int:pk>/update/', login_required(StoryUpdateView.as_view()), name="update-story"),
    path('<int:pk>/delete/', login_required(StoryDeleteView.as_view()), name="delete-story"),
    path('profile/',login_required(ProfileView.as_view()), name="user-profile"),
    path('profile/edit/',login_required(ProfileEditView.as_view()), name="user-profile-edit"),
    path('all/',login_required(AllStoriesListView.as_view()), name="all-story"),
    url(r'^accounts/', include('registration.backends.default.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

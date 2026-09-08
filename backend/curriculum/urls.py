from django.urls import path

from .views import LevelDetailView, PublicTrackListView, TrackDetailView, TrackListView

urlpatterns = [
    path("tracks/", TrackListView.as_view()),
    path("tracks/public/", PublicTrackListView.as_view()),
    path("tracks/<slug:slug>/", TrackDetailView.as_view()),
    path("levels/<int:pk>/", LevelDetailView.as_view()),
]

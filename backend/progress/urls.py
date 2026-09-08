from django.urls import path

from .views import DashboardView, HistoryView, ResetLevelView, SubmitView

urlpatterns = [
    path("challenges/<int:pk>/submit/", SubmitView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("history/", HistoryView.as_view()),
    path("levels/<int:pk>/reset/", ResetLevelView.as_view()),
]

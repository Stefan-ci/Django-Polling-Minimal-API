from polls import views
from django.urls import path

app_name = "polls"

urlpatterns = [
    path("", views.PollListView.as_view(), name="polls-list"),
    path("<str:slug>-q<int:pk>/", views.PollDetailView.as_view(), name="polls-detail"),
]

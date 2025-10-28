from django.urls import path

from . import views

urlpatterns = [
    path(
        "subscribe-to-newsletter/",
        views.SubscribeToNewsletter.as_view(),
        name="subscribe-to-newsletter",
    ),
]

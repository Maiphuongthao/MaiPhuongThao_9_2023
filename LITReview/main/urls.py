from django.urls import path

from . import views

urlpatterns = [
    path("", views.feed, name="flux"),
    path("createticket", views.create_ticket, name="new_ticket"),
    path("createreview", views.create_review, name="new_review"),
    path("ticketreview/<int:id>/", views.create_review_ticket, name="review_ticket"),
    path("posts", views.posts, name="posts"),
    path(
        "ticket/<int:pk>/delete", views.DeleteTicketView.as_view(), name="delete_ticket"
    ),
    path(
        "review/<int:pk>/delete", views.DeleteReviewView.as_view(), name="delete_review"
    ),
    path(
        "ticket/<int:pk>/update", views.UpdateTicketView.as_view(), name="update_ticket"
    ),
    path(
        "review/<int:pk>/update", views.UpdateReviewView.as_view(), name="update_review"
    ),
]

from itertools import chain

from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from .forms import ReviewForm, TicketForm
from .models import Review, Ticket

# Create your views here.


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # return queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    # cobine and sort the 2 types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    reviewed_tickets= get_reviewed_tickets()

    return render(
        request, "review/feed.html", {"posts": posts, "reviewed": reviewed_tickets,"user": request.user }
    )


def get_reviewed_tickets():
    replied_tickets = []
    reviews = Review.objects.all()
    for review in reviews:
        replied_tickets.append(review.ticket)
    return replied_tickets


def get_users_viewable_reviews(user):
    followers = get_followers(user)
    users_reviewed = []
    tickets = Ticket.objects.filter(user=user)
    for ticket in tickets:
        for review in Review.objects.all():
            if review.ticket == ticket:
                users_reviewed.append(review.user)
    reviews = Review.objects.filter(user__in=followers) | Review.objects.filter(
        user__in=users_reviewed
    )
    return reviews


def get_users_viewable_tickets(user):
    followers = get_followers(user)
    tickets = Ticket.objects.filter(user__in=followers)
    return tickets


def get_followers(user):
    # get all followers
    followers = user.following.all()
    followed_users = []
    for f in followers:
        followed_users.append(f.followed_user)
    followed_users.append(user)
    return followed_users


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                image = request.FILES.get("image", None)
                Ticket.objects.create(
                    title=request.POST["title"],
                    description=request.POST["description"],
                    user=request.user,
                    image=image,
                )
                messages.success(request, "Votre ticket est crée")
                return redirect(settings.LOGIN_REDIRECT_URL)
            except Exception as e:
                messages.error(request, f"Error {e}")
    else:
        form = TicketForm()

    return render(
        request, "review/create_ticket.html", {"form": form, "title": "Create a ticket"}
    )


@login_required
def create_review(request):
    t = TicketForm(request.POST, request.FILES)
    r = ReviewForm(request.POST)
    if request.method == "POST":
        if t.is_valid and r.is_valid:
            try:
                image = request.FILES.get("image", None)
                new_ticket = Ticket.objects.create(
                    title=request.POST["title"],
                    description=request.POST["description"],
                    user=request.user,
                    image=image,
                )
                Review.objects.create(
                    ticket=new_ticket,
                    rating=request.POST["rating"],
                    user=request.user,
                    headline=request.POST["headline"],
                    body=request.POST["body"],
                )
                messages.success(request, "Vous avez posté une critique.")
                return redirect(settings.LOGIN_REDIRECT_URL)
            except Exception as e:
                messages.error(request, f"Error {e}")
    else:
        t = TicketForm()
        r = ReviewForm()
    return render(
        request,
        "review/create_review.html",
        {"t": t, "r": r, "title": "Create a review"},
    )


@login_required
def create_review_ticket(request, id=None):
    t = get_object_or_404(Ticket, pk=id)
    r = ReviewForm(request.POST)
    if request.method == "POST":
        if r.is_valid():
            Review.objects.create(
                ticket=t,
                rating=request.POST["rating"],
                user=request.user,
                headline=request.POST["headline"],
                body=request.POST["body"],
            )
            messages.success(request, f"Vous avez crée une critque pour {t.title}")
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        r = ReviewForm()
    return render(request, "review/create_review_ticket.html", {"r": r, "t": t})


@login_required
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    reviewed = get_reviewed_tickets()
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(
        request,
        "review/posts.html",
        {"user": request.user, "posts": posts, "reviewed": reviewed},
    )


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy("posts")

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.user:
            return True
        return False


class DeleteTicketView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy("posts")

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.user:
            return True
        return False


class UpdateTicketView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy("posts")

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.user:
            return True
        return False


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy("posts")

    def test_func(self):
        review = Review.get_object()
        if self.request.user == review.user:
            return True
        return False

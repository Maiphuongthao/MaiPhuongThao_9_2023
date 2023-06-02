from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from .forms import SubscriptionsForm
from .models import UserFollows


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})


@login_required
def subscription(request):
    user = request.user
    if request.method == "POST":
        form = SubscriptionsForm(request.POST)
        if form.is_valid():
            try:
                user_to_follow = User.objects.get(
                    username=request.POST["followed_user"]
                )
                if user == user_to_follow:
                    messages.error(request, "Vous ne pouvez pas vous ajouter")
                else:
                    UserFollows.objects.create(
                        user=request.user, followed_user=user_to_follow
                    )
                    messages.success(request, f"Vous avez ajouté {user_to_follow}.")
                    return redirect("subscriptions")
            except Exception as e:
                messages.error(request, f"Error {e}")
    else:
        form = SubscriptionsForm()

    user_follows = UserFollows.objects.filter(user=request.user).order_by(
        "followed_user"
    )
    followed_by = user.followed_by.all()
    return render(
        request,
        "subscription.html",
        {
            "form": form,
            "current_user": user,
            "followed_by": followed_by,
            "user_follows": user_follows,
        },
    )


class DeleteSubscriptionView(LoginRequiredMixin, DeleteView):
    model = UserFollows
    success_url = reverse_lazy("subscriptions")
    success_message = "Abonnement supprimé"

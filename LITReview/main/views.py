from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import TicketForm
from .models import Ticket, Review

# Create your views here.

@login_required
def feed(request):
    return render(request, 'feed.html')

def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                Ticket.objects.create(title=request.POST['title'],
                                      description=request.POST['description'],
                                      user=request.user,
                                      image=request.FILES['image'])
            except Exception as e:
                messages.error(request, f"Error {e}")
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {
        'form':form,
        'title': "Create a ticket"
    })
        


from django.shortcuts import render, redirect
from .forms import TableReservationForm
from django.db.models import Sum
from django.contrib import messages
from .models import TableReservation
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')


def book_table(request):
    MAX_PEOPLE = 50  # Nombre maximal de personnes
    form = TableReservationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        reservation_date = form.cleaned_data['date']
        reservation_time = form.cleaned_data['time']

        # Calculer le nombre total de personnes déjà réservées pour cette date et heure
        total_people = \
        TableReservation.objects.filter(date=reservation_date, time=reservation_time).aggregate(sum=Sum('people'))[
            'sum'] or 0

        # Ajouter le nombre de personnes de la nouvelle réservation
        total_people += form.cleaned_data['people']

        if total_people <= MAX_PEOPLE:
            form.save()
            messages.success(request, 'Your reservation has been successfully made.')
        else:
            messages.error(request, 'Sorry, we cannot accommodate your party as it exceeds our capacity limit.')

        return redirect('index')

    return render(request, 'index.html', {'form': form})



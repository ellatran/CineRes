from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Film, Screening, Seat, Booking
from django.template import loader
from django.contrib.auth.decorators import login_required
from datetime import date


current_week=date.today().isocalendar()


# Create your views here.
def index(request):
    # Here we will see the main page and a list of available movies.
    allFilms = Film.objects.all().order_by('-id')[:3]

    template = loader.get_template('index2.html')

    context = {'films': allFilms}
    return HttpResponse(template.render(context, request))


def list_view(request):
    #List of all films
    allFilms = Film.objects.all()

    template = loader.get_template('filmslist.html')

    context = {'films': allFilms}
    return HttpResponse(template.render(context, request))


def detail(request, pk):
    # This is the page opens after you click a the link of a film
    filmInfo = Film.objects.get(pk=pk)
    template = loader.get_template('detail.html')
    return HttpResponse(template.render({'filmInfo': filmInfo}, request))


@login_required(login_url='/accounts/login')
def screenings(request, pk):
    if request.method == 'POST':
        return redirect('reservation:seat_selection', request.POST['scrID'])
    else:
        Screenings = Screening.objects.filter(film=pk).order_by('date_time')
        filmInfo = Film.objects.get(pk=pk)
        template = loader.get_template('get_screening.html')
        return HttpResponse(template.render({'filmInfo': filmInfo, 'Screenings': Screenings}, request))


@login_required(login_url='/accounts/login')
def seat_selection(request, scrID):
    # seat map will be shown
    if request.method == 'POST':
        book = Booking.objects.create(Screening_id=scrID, customer=request.user)
        b_id = book.id
        seatlist = request.POST.getlist('seat')
        for item in seatlist:
            to_upd = Seat.objects.get(id=item)
            to_upd.Status = 'RSV'
            to_upd.booking_id = b_id
            to_upd.save()
        return redirect('reservation:booking', b_id)
    else:
        screen = Screening.objects.get(id=scrID)

        letters = "ABCDEFGHIJ"
        numbers = range(1, 25)
        seats = Seat.objects.filter(Screening=scrID)
        context = {'seats': seats, 'letters': letters, 'numbers': numbers, 'screen': screen}
        template = loader.get_template('seat_selection.html')
        return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login')
def booking(request, b_id):
    resv = Booking.objects.get(pk=b_id)
    seating = Seat.objects.filter(booking_id=b_id)
    context = {'resv': resv, 'seating': seating}
    template = loader.get_template('booking.html')
    return HttpResponse(template.render(context, request))

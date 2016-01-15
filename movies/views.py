from datetime import datetime, timedelta

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponseNotFound, HttpResponseBadRequest

from .models import Movie, Tickets, MovieForm, TicketsForm
from .tasks import unbook_ticket_task

def index(request):
    """
    Homepage view
    :param request:
    :return:
    """
    current_movies = Movie.objects.all()
    context = {
        'current_movies': current_movies,
        'form': MovieForm(),
        'cart': request.session.get('cart', [])
    }
    return render(request, "index.html", context)


def new_movie(request):
    """
    Create a new movie from the form information
    :param request:
    :return:
    """
    f = MovieForm(request.POST)
    f.save()
    return redirect('home')


def movie_detail(request, movie_id=None):
    """
    Get details of movie and book/reserve ticket
    :param request:
    :param movie_id:
    :return:
    """
    try:
        movie = Movie.objects.get(pk=movie_id)
        tickets_booked = Tickets.objects.filter(movie=movie)
        context = {
            'movie': movie,
            'tickets_booked': tickets_booked,
            'ticket_form': TicketsForm(),
            'cart': request.session.get('cart', [])
        }
        return render(request, "movie.html", context)
    except Movie.DoesNotExist:
        return HttpResponseNotFound('<h1>This movie does not exist</h1>')


def book_ticket(request, movie_id=None):
    """
    Book a ticket
    :param request:
    :param movie_id:
    :return:
    """
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return HttpResponseNotFound('<h1>This movie does not exist</h1>')

    cart = request.session.get('cart', [])
    f = TicketsForm(request.POST)
    ticket = f.save(commit=False)
    ticket.movie = movie

    if ticket.row_num == 0 or ticket.col_num == 0 or ticket.row_num > movie.rows or ticket.col_num > movie.columns:
        return HttpResponseBadRequest("Invalid ticket number")

    if not request.session.session_key:
        request.session.save()
    ticket.session = request.session.session_key

    try:
        existing_tix = Tickets.objects.get(row_num=ticket.row_num, col_num=ticket.col_num, movie=movie)
        if existing_tix.session == ticket.session or existing_tix.status == 1:
            if existing_tix.status == 1:
                existing_tix.delete()
            else:
                ticket = existing_tix
        else:
            return HttpResponseBadRequest("This ticket has already been reserved")
    except Tickets.DoesNotExist:
        pass

    should_spawn_background_thread = False

    if 'book_tix' in request.POST:
        ticket.status = 3
    elif 'block_tix' in request.POST:
        if ticket.status == 1:
            should_spawn_background_thread = True
            print "Spawning now"
        ticket.status = 2

    ticket.save()
    if should_spawn_background_thread:
        three_mins_hence = datetime.utcnow() + timedelta(minutes=3)
        unbook_ticket_task.apply_async((ticket.id,), eta=three_mins_hence)

    cart_set = set(cart)
    cart_set.add(ticket.pk)
    cart = list(cart_set)
    request.session['cart'] = cart
    request.session.save()

    return redirect('movie', movie_id=movie_id)


def modify_ticket(request, ticket_id=None, action=None):
    """
    Modify a ticket
    :param request:
    :param ticket_id:
    :return:
    """
    try:
        ticket = Tickets.objects.get(id=ticket_id)
        movie_id = ticket.movie.id
        if action == 'cancel':
            cart = request.session.get('cart', [])
            cart_set = set(cart)
            cart_set.discard(ticket.pk)
            cart = list(cart_set)

            request.session['cart'] = cart

            ticket.delete()
        elif action == 'book':
            ticket.status = 3
            ticket.save()

    except Tickets.DoesNotExist:
        return HttpResponseBadRequest("Can't find this ticket")

    return redirect('movie', movie_id=movie_id)


def shopping_cart(request, movie_id=None):
    """
    View to render current shopping cart
    :param request:
    :param movie_id:
    :return:
    """
    cart = request.session.get('cart', [])
    tickets = Tickets.objects.filter(id__in=cart)
    context = {
        'tickets': tickets,
        'cart': cart
    }

    return render(request, 'shopping_cart.html', context)
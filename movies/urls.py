from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^new_movie/$', views.new_movie,),
    url(r'^book_ticket/(?P<movie_id>\d+)/$', views.book_ticket, name="book_ticket"),
    url(r'^modify_ticket/(?P<ticket_id>\d+)/(?P<action>[\w-]+)/$', views.modify_ticket, name="modify_ticket"),
    url(r'^movie/(?P<movie_id>\d+)/$', views.movie_detail, name="movie"),
    url(r'^shopping_cart/$', views.shopping_cart, name='cart')
]
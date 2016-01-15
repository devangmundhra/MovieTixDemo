from __future__ import absolute_import

from celery import shared_task

from .models import Tickets

@shared_task
def unbook_ticket_task(ticket_id):
    print "Unbooking now"
    try:
        ticket = Tickets.objects.get(pk=ticket_id)
        ticket.status = 1
        ticket.save()
    except Tickets.DoesNotExist:
        pass
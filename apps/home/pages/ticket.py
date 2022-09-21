from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django import forms
from helpdesk.models import Queue, Ticket, FollowUp
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from helpdesk.serializers import TicketSerializer


class CreateTicketForm(forms.Form):
    queue = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=('Select Category'),
        required=True,
        choices=Queue.objects.filter(
            allow_public_submission=True).values_list("id", "title")
    )

    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', "placeholder": "Subject"}),
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', "placeholder": "Message"}),
        required=True
    )

    class Meta:
        model = Ticket


@login_required(login_url="/login/")
def createTicket(request):
    form = CreateTicketForm(request.POST)
    data = request.POST
    context = {"message": "", "success": True}
    if form.is_valid():
        ticket = Ticket.objects.create(queue=Queue.objects.get(id=data["queue"]), title=data["title"], description=data["description"],
                                       priority=5, status=1, assigned_to=request.user)
        ticket.save()
    else:
        context["success"] = False
    return JsonResponse(context, safe=False)


@login_required(login_url="/login/")
def closeTicket(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.status = 4
    ticket.save()
    return JsonResponse({"success": True}, safe=False)


@login_required(login_url="/login/")
def followTicket(request, id):
    message = request.POST['message']
    ticket = Ticket.objects.get(id=id)
    follow = FollowUp.objects.create(
        ticket=ticket, user=request.user, comment=message, title="Reply from user", public=True)
    follow.save()
    return JsonResponse({"success": True}, safe=False)


@login_required(login_url="/login/")
def readTicket(request, id):
    ticket = Ticket.objects.get(id=id)
    content = TicketSerializer(ticket)
    return JsonResponse(content.data, safe=False)


@login_required(login_url="/login/")
def getTicketsTable(request):
    context = {
        "tickets": Ticket.objects.order_by("-modified").filter(Q(assigned_to=request.user) | Q(assigned_to=None)).all(),
        "len_tickets": len(Ticket.objects.order_by("-modified").filter(Q(assigned_to=request.user) | Q(assigned_to=None)).all()),
    }
    html_template = loader.get_template('helpdesk/tickets_table.html')
    return HttpResponse(html_template.render(context, request))

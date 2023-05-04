from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from item.models import Item
# Create your views here.

@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)

    ctx = {
        'items': items
    }
    return render(request, 'dashboard/index.html', ctx)

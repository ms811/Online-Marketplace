from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, Category
from .forms import NewItemForm, EditItemForm

# Create your views here.
def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id = category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    ctx = {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    }

    return render(request, 'item/items.html', ctx)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category = item.category, is_sold=False).exclude(pk=pk)[0:3]

    ctx = {
        'item': item,
        'related_items': related_items,
    }
    return render(request, 'item/detail.html', ctx)

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            # At this point the created by is not filled in and so we use commit False so that
            # the item is not saved but an object is created.
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
        
    ctx = {
        'form': form,
        'title': 'New item',
    }

    return render(request, 'item/form.html', ctx)

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            # At this point the created by is not filled in and so we use commit False so that
            # the item is not saved but an object is created.
            form.save() 

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
        
    ctx = {
        'form': form,
        'title': 'Edit item',
    }

    return render(request, 'item/form.html', ctx)

@login_required
def delete(request, pk):    
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')
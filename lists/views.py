﻿from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List

def home_page(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
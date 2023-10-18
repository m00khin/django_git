from django.shortcuts import render, redirect
# from django.http import HttpResponse
from . models import Mebel
from . forms import UpdateItemForm


def show_all(request):
    mebels = Mebel.objects.all().order_by("-price")
    return render(
        request,
        'app_1/show_all.html',
        {'mebels': mebels}
    )


def show_all_admin(request):
    form = UpdateItemForm()
    mebels = Mebel.objects.all().order_by("-price")
    return render(
        request,
        'app_1/show_admin_item.html',
        {
            'form': form,
            'mebels': mebels
        }
    )


def show_item(request, item_id):
    item = Mebel.objects.get(pk=item_id)
    return render(
        request,
        'app1/show_item.html',
        {'item': item}
    )


def update_item(request, item_id):
    if request.method == 'POST':
        new_description = dict(request.POST).get('description', '')
        new_price = dict(request.POST).get('price', '')
        Mebel.objects.filter(pk=item_id).update(
            price=new_price[0],
            description=new_description[0]
        )
    return redirect('admin')


def delete_item(request, item_id):
    Mebel.objects.filter(pk=item_id).delete()
    return redirect('admin')


def main(request):
    return redirect('main')


def page_not_found(request, *args, **argv):
    return redirect('main')

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import request, HttpResponse, JsonResponse


def place_order(request):
    context = {'font_flag': 'place_order'}
    return render(request, 'df_order/place_order.html', context)

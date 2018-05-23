from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import request, HttpResponse, JsonResponse


def cart(request):
    context = {'font_flag': 'cart'}
    return render(request, 'df_cart/cart.html', context)


from django.shortcuts import render
from django.utils.translation import ugettext as _


def home(request):
    return render(request, 'home.html', {'title': _('Home')})

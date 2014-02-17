# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from allauth.account import views as authviews
from series_watcher.models import Series, Episode
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.utils import simplejson


def home(request):
    if request.user.is_authenticated():
        watched_episodes = request.user.episode_set.order_by(
            'season__series__name',
            'season__number', 'number', 'name').all()
    else:
        watched_episodes = []
    return render(request, 'home.html', {
        'title': _('Home'),
        'episodes': watched_episodes})


@login_required
def series(request):
    series = Series.objects.order_by('name').all()
    return render(request, 'series.html', {
        'title': _('Series'),
        'series': series})


@login_required
@csrf_protect
@require_POST
def toggle_subscription(request):
    output = {}
    serie_id = request.POST.get('sid', 0)
    if serie_id == 0:
        output = {'result': 'failure'}
    else:
        serie = Series.objects.get(id=serie_id)
        # If the user has subscribed to the series, unsubscribe
        if serie in request.user.series_set.all():
            request.user.series_set.remove(serie)
            text = 'Subscribe'
        # If he hasn't subscribed, subscribe
        else:
            request.user.series_set.add(serie)
            text = 'Unsubscribe'
        output = {'result': 'success',
                  'text': text}
    output_json = simplejson.dumps(output)
    return HttpResponse(output_json, mimetype="application/json")


@login_required
@csrf_protect
@require_POST
def remove_watch(request):
    episode_id = request.POST.get('epid', 0)
    if episode_id == 0:
        output = {'result': 'failure'}
    else:
        episode = Episode.objects.get(id=episode_id)
        request.user.episode_set.remove(episode)
        output = {'result': 'success'}
    output_json = simplejson.dumps(output)
    return HttpResponse(output_json, mimetype="application/json")


# Override the LoginView from allauth
class LoginView(authviews.LoginView):
    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        ret.update({'title': _('Log in')})
        return ret
login = LoginView.as_view()


# Override the SignupView from allauth
class SignupView(authviews.SignupView):
    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        ret.update({'title': _('Sign up')})
        return ret
signup = SignupView.as_view()


# Override the LogoutView from allauth
class LogoutView(authviews.LogoutView):
    def get_context_data(self, **kwargs):
        ret = super(LogoutView, self).get_context_data(**kwargs)
        ret.update({'title': _('Log out')})
        return ret
logout = LogoutView.as_view()


# Override the PasswordResetView from allauth
class PasswordResetView(authviews.PasswordResetView):
    def get_context_data(self, **kwargs):
        ret = super(PasswordResetView, self).get_context_data(**kwargs)
        ret.update({'title': _('Password reset')})
        return ret
password_reset = PasswordResetView.as_view()

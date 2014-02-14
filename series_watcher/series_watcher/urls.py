from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'series_watcher.views.home', name='home'),
    url(r'^series/$', 'series_watcher.views.series', name='series'),
    url(r'^toggle_subscription/$',
        'series_watcher.views.toggle_subscription',
        name='toggle_subscription'),
    url(r'^remove_watch/$',
        'series_watcher.views.remove_watch',
        name='remove_watch'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'series_watcher.views.login',
        name='account_login'),
    url(r'^accounts/signup/$', 'series_watcher.views.signup',
        name='account_signup'),
    url(r'^accounts/logout/$', 'series_watcher.views.logout',
        name='account_logout'),

    # Password reset
    url(r"^password/reset/$",
        'series_watcher.views.password_reset',
        name="account_reset_password"),
    url(r"^password/reset/done/$",
        'allauth.account.views.password_reset_done',
        name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        'allauth.account.views.password_reset_from_key',
        name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$",
        'allauth.account.views.password_reset_from_key_done',
        name="account_reset_password_from_key_done"),


    # url(r'^accounts/', include('allauth.urls')),

    # Examples:
    # url(r'^series_watcher/', include('series_watcher.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)

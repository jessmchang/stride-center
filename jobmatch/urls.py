from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jobmatch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^dashboard/', 'jobmatch.views.dashboard'),
    url(r'^profile/', 'jobmatch.views.profile'),
    url(r'^register/', 'jobmatch.views.create_user'),
    url(r'^$', 'jobmatch.views.index'),
)

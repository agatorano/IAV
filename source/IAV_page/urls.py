from django.conf.urls import patterns,url

urlpatterns = patterns('',
    url(r'^$','IAV_page.views.IAV_home',name='IAV_home'),
    url(r'^(\d+)/$', 'IAV_page.views.view_IAV',name='view_IAV'),
    url(r'^new$', 'IAV_page.views.new_IAV', name = 'new_IAV'),
    )

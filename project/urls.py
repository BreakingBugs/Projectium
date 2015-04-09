from django.conf.urls import patterns, url
from project import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^users/$', views.UserList.as_view(), name='user_list'),
                       url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user_detail'),
                       url(r'^users/add/$', views.AddUser.as_view(), name="user_add"),
                       url(r'^users/(?P<pk>\d+)/delete/$', views.DeleteUser.as_view(), name="user_delete"),
                       url(r'^users/(?P<pk>\d+)/edit/$', views.UpdateUser.as_view(), name="user_update"),
                       url(r'^projects/$', views.ProjectList.as_view(), name='project_list'),
                       url(r'^projects/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project_detail'),
                       url('^login/$', 'django.contrib.auth.views.login', name='login'),
                       url('^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       url('^password_change/$', 'django.contrib.auth.views.password_change',
                           {'post_change_redirect': '/', 'template_name': 'project/password_change.html'},
                           name='password_change'),
                       url('^roles/$', views.RolList.as_view(), name='rol_list'),
                       url(r'^roles/(?P<pk>\d+)/$', views.RolDetail.as_view(), name='rol_detail'),
                       url(r'^roles/add/$', views.AddRolView.as_view(), name="rol_add"),
                       url(r'^roles/(?P<pk>\d+)/edit/$', views.UpdateRolView.as_view(), name="rol_update"),
                       url(r'^roles/(?P<pk>\d+)/delete/$', views.DeleteRolView.as_view(), name="rol_delete"),
                       url(r'^flujo/$',views.FlujoList.as_view(),name='flujo_list'),
                       url(r'^flujo/(?P<pk>\d+)/$', views.FlujoDetail.as_view(), name='flujo_detail'),
                       url(r'^flujo/add/$', views.AddFlujo.as_view(), name="flujo_add")
                       )

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
                       url(r'^projects/cancelled/$', views.ProjectList.as_view(show_cancelled=True), name='project_list_cancelled'),
                       url(r'^projects/add/$', views.ProjectCreate.as_view(), name='project_create'),
                       url(r'^projects/(?P<pk>\d+)/edit/$', views.ProjectUpdate.as_view(), name='project_update'),
                       url(r'^projects/(?P<pk>\d+)/delete/$', views.ProjectDelete.as_view(), name='project_delete'),
                       url(r'^projects/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project_detail'),
                       url(r'^projects/(?P<project_pk>\d+)/flujo/$',views.FlujoList.as_view(),name='flujo_list'),
                       url(r'^flujo/(?P<pk>\d+)/$', views.FlujoDetail.as_view(), name='flujo_detail'),
                       url(r'^projects/(?P<project_pk>\d+)/flujo/add/$', views.AddFlujo.as_view(), name="flujo_add"),
                       url(r'^projects/(?P<project_pk>\d+)/flujo/addfromtemplate/$', views.CreateFromPlantilla.as_view(), name="flujo_addfromtemplate"),
                       url(r'^flujo/(?P<pk>\d+)/edit/$', views.UpdateFlujo.as_view(), name="flujo_update"),
                       url(r'^flujo/(?P<pk>\d+)/delete/$', views.DeleteFlujo.as_view(), name="flujo_delete"),
                       url('^roles/$', views.RolList.as_view(), name='rol_list'),
                       url(r'^roles/(?P<pk>\d+)/$', views.RolDetail.as_view(), name='rol_detail'),
                       url(r'^roles/add/$', views.AddRolView.as_view(), name="rol_add"),
                       url(r'^roles/(?P<pk>\d+)/edit/$', views.UpdateRolView.as_view(), name="rol_update"),
                       url(r'^roles/(?P<pk>\d+)/delete/$', views.DeleteRolView.as_view(), name="rol_delete"),


                       #TODO: mover la logica de autenticacion
                       url('^login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'authentication/login.html'}, name='login'),
                       url('^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       url('^password_change/$', 'django.contrib.auth.views.password_change',
                           {'post_change_redirect': '/', 'template_name': 'authentication/password_change.html'},
                           name='password_change'),
                       url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
                           {'post_reset_redirect': 'project:password_reset_done', 'template_name': 'authentication/password_reset_form.html',
                            'email_template_name': 'authentication/password_reset_email.html'}, name='password_reset'),
                       url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
                           {'template_name': 'authentication/password_reset_done.html'}, name='password_reset_done'),
                       url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           {'template_name': 'authentication/password_reset_confirm.html','post_reset_redirect': 'project:password_reset_complete'},
                           name='password_reset_confirm'),
                       url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
                           {'template_name': 'authentication/password_reset_complete.html'}, name='password_reset_complete'),
                       
                       url(r'^plantilla/$',views.PlantillaList.as_view(),name='plantilla_list'),
                       url(r'^plantilla/(?P<pk>\d+)/$', views.PlantillaDetail.as_view(), name='plantilla_detail'),
                       url(r'^plantilla/add/$', views.AddPlantilla.as_view(), name="plantilla_add"),
                       url(r'^plantilla/(?P<pk>\d+)/delete/$', views.DeletePlantilla.as_view(), name="plantilla_delete"),
                       url(r'^plantilla/(?P<pk>\d+)/edit/$', views.UpdatePlantilla.as_view(), name="plantilla_update"),
                       url(r'^projects/(?P<project_pk>\d+)/sprint/add/$', views.AddSprintView.as_view(), name="sprint_add"),
                       url(r'^sprint/(?P<pk>\d+)/$', views.SprintDetail.as_view(), name='sprint_detail'),
                       )

# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from guardian.mixins import PermissionRequiredMixin, LoginRequiredMixin
from guardian.admin import *;
from project.models import MiembroEquipo, Proyecto, UserStory, Adjunto


class GlobalPermissionRequiredMixin(PermissionRequiredMixin):
    '''
    Mixin que permite requerir un permiso
    '''
    accept_global_perms = True
    return_403 = True
    raise_exception = True


class CreateViewPermissionRequiredMixin(GlobalPermissionRequiredMixin):
    '''
    Mixin que permite requerir un permiso
    '''

    def get_object(self):
        return None


class ActiveProjectRequiredMixin(object):
    proyecto = None

    def get_proyecto(self):
        return self.proyecto

    def dispatch(self, request, *args, **kwargs):
        proyecto = self.get_proyecto()
        if proyecto.estado != 'AP':
            return super(ActiveProjectRequiredMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()

@login_required()
def home(request):
    """
    Vista para la pantalla principal.
    """
    context = {}
    context['users'] = User.objects.all()
    context['proyects'] = Proyecto.objects.all()
    context['team_members'] = MiembroEquipo.objects.all()

    return render(request, 'project/home.html', context)


def get_selected_perms(POST):
    """
    Obtener los permisos marcados en el formulario

    :param POST: diccionario con los datos del formulario
    :return: lista de permisos
    """
    current_list = POST.getlist('perms_proyecto')
    current_list.extend(POST.getlist('perms_userstory'))
    current_list.extend(POST.getlist('perms_flujo'))
    current_list.extend(POST.getlist('perms_sprint'))
    return current_list
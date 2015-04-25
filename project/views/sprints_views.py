# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms.extras import SelectDateWidget
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from guardian.mixins import LoginRequiredMixin
from guardian.shortcuts import get_perms
from project.forms import AddToSprintForm, AddToSprintFormset
from project.models import Sprint, Proyecto, Actividad, Flujo, UserStory
from project.views import CreateViewPermissionRequiredMixin, GlobalPermissionRequiredMixin
from django.views import generic
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime

class SprintList(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.ListView):
    """
    Vista de Listado de Sprint en el sistema
    """
    model = Sprint
    template_name = 'project/sprint/sprint_list.html'
    permission_required = 'project.view_project'
    context_object_name = 'sprint'
    project = None

    def get_permission_object(self):
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return self.project

    def get_context_data(self, **kwargs):
        context = super(SprintList, self).get_context_data(**kwargs)
        context['proyecto_perms'] = get_perms(self.request.user, self.project)
        return context

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        self.project = get_object_or_404(Proyecto, pk=project_pk)
        return Sprint.objects.filter(proyecto=self.project)

class SprintDetail(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DetailView):
    """
    Vista del detalle de un Sprint en el sistema
    """
    model = Sprint
    permission_required = 'project.view_project'
    template_name = 'project/sprint/sprint_detail.html'
    context_object_name = 'sprint'

    def get_permission_object(self):
        return self.get_object().proyecto

    def get_context_data(self, **kwargs):
        context = super(SprintDetail, self).get_context_data(**kwargs)
        context['userStory'] = self.object.userstory_set.all()
        return context



class AddSprintView(LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    Vista para agregar un Sprint en el sistema y añadir este sprint, un desarrollador y una actividad al user Story
    """
    model = Sprint
    template_name = 'project/sprint/sprint_form.html'
    permission_required = 'project.create_sprint'
    form_class = modelform_factory(Sprint,
                                   widgets={'inicio': SelectDateWidget},
                                   fields={'nombre', 'inicio'})
    formset = formset_factory(AddToSprintForm, formset=AddToSprintFormset, extra=1)

    proyecto = None

    def get_permission_object(self):
        return get_object_or_404(Proyecto, id=self.kwargs['project_pk'])

    def get_success_url(self):
        return reverse('project:sprint_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AddSprintView, self).get_context_data(**kwargs)
        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['project_pk'])
        formset=self.formset()
        for userformset in formset.forms:
            userformset.fields['desarrollador'].queryset = User.objects.filter(miembroequipo__proyecto=self.proyecto)
            userformset.fields['flujo'].queryset = Flujo.objects.filter(proyecto=self.proyecto)
            userformset.fields['userStory'].queryset = UserStory.objects.filter(proyecto=self.proyecto)
        context['formset'] = formset
        return context



    def form_valid(self, form):
        """
        Guarda el desarrollador, actividad y sprint asociado al un projecto dentro de un User Story
        :param form: formulario del sprint
        :return: vuelve a la pagina de detalle del sprint
        """

        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['project_pk'])
        self.object= form.save(commit=False)
        self.object.proyecto= self.proyecto
        self.object.fin= self.object.inicio + datetime.timedelta(days=self.proyecto.duracion_sprint)
        self.object.save()
        formsetb= self.formset(self.request.POST)
        if formsetb.has_changed():
            if formsetb.is_valid():
                for subform in formsetb :
                    new_userStory = subform.cleaned_data['userStory']
                    new_flujo = subform.cleaned_data['flujo']
                    self.flujo = new_flujo
                    new_desarrollador = subform.cleaned_data['desarrollador']
                    new_userStory.desarrollador= new_desarrollador
                    new_userStory.sprint= self.object
                    new_userStory.actividad=self.flujo.actividad_set.first()
                    new_userStory.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return render(self.request, self.get_template_names(), {'form': form, 'formset': formsetb},
                      context_instance=RequestContext(self.request))
        else:
            return HttpResponseRedirect(self.get_success_url())


class UpdateSprintView(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.UpdateView):
    """
    Vista para actualizar los datos del Sprint y  del UserStory que son el desarrollador, la actividad y el Sprint
    """
    model = Sprint
    permission_required = 'project.edit_sprint'
    template_name = 'project/sprint/sprint_form.html'
    form_class = modelform_factory(Sprint,
                                   widgets={'inicio': SelectDateWidget},
                                   fields={'nombre', 'inicio'})
    UserStoryFormset = formset_factory(AddToSprintForm, formset=AddToSprintFormset, can_delete=True, extra=1)
    formset = None

    def get_permission_object(self):
        """
        permiso para add, edit o delete
        :return: los permisos
        """
        return self.get_object().proyecto

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del sprint agregado.
        """
        return reverse('project:sprint_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        """
        Especifica los datos de contexto a pasar al template
        :param kwargs: Diccionario con parametros con nombres clave
        :return: los datos de contexto
        """
        context= super(UpdateSprintView,self).get_context_data(**kwargs)
        current_us = self.get_object().userstory_set.all()
        formset= self.UserStoryFormset(initial=[{'userStory':us, 'flujo':us.actividad.flujo, 'desarrollador':us.desarrollador} for us in current_us])
        for userformset in formset.forms:
            userformset.fields['desarrollador'].queryset = User.objects.filter(miembroequipo__proyecto=self.object.proyecto)
            userformset.fields['flujo'].queryset = Flujo.objects.filter(proyecto=self.object.proyecto)
            userformset.fields['userStory'].queryset = UserStory.objects.filter(proyecto=self.object.proyecto)
        context['formset'] = formset
        return context

    def form_valid(self, form):
        """
        Guarda el desarrollador, actividad y sprint asociado al un projecto dentro de un User Story
        :param form: formulario del sprint
        :return: vuelve a la pagina de detalle del sprint
        """

        self.object= form.save(commit=False)
        self.object.fin= self.object.inicio + datetime.timedelta(days=self.object.proyecto.duracion_sprint)
        self.object.save()
        formsetb= self.UserStoryFormset(self.request.POST)
        if formsetb.is_valid():
            for subform in formsetb:
                if subform.has_changed() and 'userStory' in subform.cleaned_data:
                    print(subform.cleaned_data)
                    new_userStory = subform.cleaned_data['userStory']
                    if subform in formsetb.deleted_forms:
                        # desaciamos los user story que se eliminaron del form
                        new_userStory.desarrollador = None
                        new_userStory.sprint = None
                        new_userStory.actividad = None
                    else:
                        new_flujo = subform.cleaned_data['flujo']
                        self.flujo = new_flujo
                        new_desarrollador = subform.cleaned_data['desarrollador']
                        new_userStory.desarrollador = new_desarrollador
                        new_userStory.sprint = self.object
                        new_userStory.actividad = self.flujo.actividad_set.first()
                    new_userStory.save()
            return HttpResponseRedirect(self.get_success_url())

        return render(self.request, self.get_template_names(), {'form': form, 'formset': formsetb},
                      context_instance=RequestContext(self.request))
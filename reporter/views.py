from django.views.generic import TemplateView
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.db import transaction

from . import models
from .forms import ReportForm, ReportUpdateForm

from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from django.db.models import Count, F, Q, Sum, Max, Prefetch

# reporter/utils/
from .utils.ai_extraction import extract_ai_fields_from_images
from .utils.report_matching import apply_match_scores


class CreateReport(generic.CreateView):
    form_class = ReportForm
    model = models.Report

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)

            # Make sure we have a front image; adjust field name if your form uses something else
            uploaded_front = self.request.FILES.get('front_image')
            if not uploaded_front:
                form.add_error('front_image', 'Front label image is required.')
                return self.form_invalid(form)

            # First save so the ImageFields are written to disk
            self.object.save()

            front_path = self.object.front_image.path if self.object.front_image else None
            back_path = self.object.back_image.path if self.object.back_image else None

            # Call OpenAI to fill ai_* fields from images
            ai_data = extract_ai_fields_from_images(front_path, back_path)

            for field, value in ai_data.items():
                setattr(self.object, field, value)

            apply_match_scores(self.object)

            # Save with AI fields populated
            self.object.save()

        # Let the normal CreateView flow handle redirects etc.
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('reporter:single', kwargs={
            'slug': self.object.slug
        })


class ReportList(generic.ListView):
    model = models.Report
    paginate_by = 7


    def get_context_data(self, **kwargs):
        context = super(ReportList, self).get_context_data(**kwargs)

        context['Gsearch'] = self.request.GET.get('Gsearch', '')

        return context

    def get_queryset(self):

        query = self.request.GET.get('Gsearch', '').strip()

        # Base queryset
        object_list = self.model.objects.all()

        filters = {}
        ordering = ['-last_modified', 'product_name']

        if query:
            object_list = object_list.filter(
                Q(brand__icontains=query) |
                Q(ai_brand__icontains=query) |
                Q(product_name__icontains=query) |
                Q(ai_product_name__icontains=query) |
                Q(product_type__icontains=query) |
                Q(milliliters__icontains=query) |
                Q(fl_oz__icontains=query)
            )


        object_list = object_list.filter(**filters).order_by(*ordering)
        paginator = Paginator(object_list, self.paginate_by)

        return object_list




class ReportDetail(generic.DetailView):
    model = models.Report


    # makes sure the queryset matches the username exactly
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(slug__iexact=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super(ReportDetail,self).get_context_data(**kwargs)

        file = self.get_object()


        return context


class UpdateReportView(generic.UpdateView):
    form_class = ReportUpdateForm
    model = models.Report
    template_name = 'reporter/report_update.html'

    def get_object(self):

        return get_object_or_404(Report, slug__iexact=self.kwargs.get("slug"), pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.save()

        messages.success(self.request, 'Your Report was updated')
        return super().form_valid(form)



    def form_invalid(self, form):
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            return super().form_invalid(form)

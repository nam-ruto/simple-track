from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Application
from .forms import ApplicationForm


@login_required
def application_list(request):
    applications = Application.objects.filter(user=request.user)

    kanban_columns = [
        {
            'key': 'APPLIED',
            'label': 'Applied',
            'color': 'primary',
            'icon': 'bi-send',
            'items': applications.filter(status='APPLIED'),
        },
        {
            'key': 'INTERVIEWED',
            'label': 'Interviewed',
            'color': 'warning',
            'icon': 'bi-people',
            'items': applications.filter(status='INTERVIEWED'),
        },
        {
            'key': 'OFFER',
            'label': 'Offer',
            'color': 'success',
            'icon': 'bi-trophy',
            'items': applications.filter(status='OFFER'),
        },
        {
            'key': 'REJECTED',
            'label': 'Rejected',
            'color': 'danger',
            'icon': 'bi-x-circle',
            'items': applications.filter(status='REJECTED'),
        },
    ]

    return render(request, 'applications/application_list.html', {
        'kanban_columns': kanban_columns,
        'total': applications.count(),
    })


def _wants_partial(request):
    """True when the request comes from the modal (JS fetch)."""
    return (
        request.GET.get('partial') == '1'
        or request.POST.get('partial') == '1'
    )


@login_required
def application_create(request):
    partial = _wants_partial(request)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            if partial:
                return JsonResponse({'success': True})
            messages.success(
                request,
                f'Application for <strong>{application.job_title}</strong> at <strong>{application.company}</strong> added!',
            )
            return redirect('application_list')
        elif partial:
            return render(
                request,
                'applications/application_form_partial.html',
                {'form': form, 'action': 'Create', 'form_action': reverse('application_create')},
                status=422,
            )
    else:
        form = ApplicationForm()

    if partial:
        return render(
            request,
            'applications/application_form_partial.html',
            {'form': form, 'action': 'Create', 'form_action': reverse('application_create')},
        )

    return render(request, 'applications/application_form.html', {
        'form': form,
        'action': 'Create',
        'page_title': 'Add New Application',
    })


@login_required
def application_edit(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    partial = _wants_partial(request)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            if partial:
                return JsonResponse({'success': True})
            messages.success(request, 'Application updated successfully!')
            return redirect('application_list')
        elif partial:
            return render(
                request,
                'applications/application_form_partial.html',
                {'form': form, 'action': 'Edit', 'form_action': reverse('application_edit', args=[pk])},
                status=422,
            )
    else:
        form = ApplicationForm(instance=application)

    if partial:
        return render(
            request,
            'applications/application_form_partial.html',
            {'form': form, 'action': 'Edit', 'form_action': reverse('application_edit', args=[pk])},
        )

    return render(request, 'applications/application_form.html', {
        'form': form,
        'action': 'Edit',
        'page_title': f'Edit: {application.job_title}',
        'application': application,
    })


@login_required
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == 'POST':
        title = str(application)
        application.delete()
        messages.success(request, f'Application for <strong>{title}</strong> deleted.')
        return redirect('application_list')

    return render(request, 'applications/application_confirm_delete.html', {
        'application': application,
    })


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    return render(request, 'applications/application_detail.html', {
        'application': application,
    })


@login_required
@require_POST
def application_update_status(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    new_status = request.POST.get('status', '')
    valid = [s[0] for s in Application.STATUS_CHOICES]
    if new_status in valid:
        application.status = new_status
        application.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)

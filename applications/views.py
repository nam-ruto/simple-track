from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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


@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, f'Application for <strong>{application.job_title}</strong> at <strong>{application.company}</strong> added!')
            return redirect('application_list')
    else:
        form = ApplicationForm()

    return render(request, 'applications/application_form.html', {
        'form': form,
        'action': 'Create',
        'page_title': 'Add New Application',
    })


@login_required
def application_edit(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f'Application updated successfully!')
            return redirect('application_list')
    else:
        form = ApplicationForm(instance=application)

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

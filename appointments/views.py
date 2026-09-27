from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm


@login_required
def appointment_list(request):
    status = request.GET.get('status', '')

    if request.user.role == 'doctor':
        appointments = Appointment.objects.filter(
            doctor__user=request.user
        ).select_related('patient', 'doctor__user')
    else:
        appointments = Appointment.objects.select_related(
            'patient', 'doctor__user'
        ).all()

    if status:
        appointments = appointments.filter(status=status)

    all_statuses = list(Appointment.STATUS_CHOICES)

    return render(request, 'appointments/list.html', {
        'appointments': appointments,
        'all_statuses': all_statuses,
        'selected': status
    })

@login_required
def appointment_add(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        try:
            if form.is_valid():
                appointment = form.save()
                messages.success(
                    request,
                    f'Appointment booked successfully!'
                )
                return redirect('appointment_list')
            else:
                messages.error(request, 'Please fix the errors below.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/form.html', {
        'form'  : form,
        'action': 'Book Appointment'
    })


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Appointment updated!')
                return redirect('appointment_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/form.html', {
        'form'       : form,
        'appointment': appointment,
        'action'     : 'Update Appointment'
    })


@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled.')
        return redirect('appointment_list')
    return render(request, 'appointments/confirm_cancel.html', {
        'appointment': appointment
    })
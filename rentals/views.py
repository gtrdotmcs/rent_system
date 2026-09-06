from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Property, Lease, Payment
from .forms import LeaseForm, PaymentForm

def owner_required(view_func):
    """Decorator to ensure only OWNER can access the view."""
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "OWNER":
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

def tenant_required(view_func):
    """Decorator to ensure only TENANT can access the view."""
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "TENANT":
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

@login_required
@owner_required
def property_list(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'rentals/property_list.html', {'properties': properties})

@login_required
@owner_required
def property_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        description = request.POST.get('description', '')
        
        Property.objects.create(
            owner=request.user,
            name=name,
            address=address,
            city=city,
            description=description
        )
        messages.success(request, "Property created successfully")
        return redirect('property_list')
        
    return render(request, 'rentals/property_form.html')

@login_required
@owner_required
def property_edit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property_obj.name = request.POST.get('name')
        property_obj.address = request.POST.get('address')
        property_obj.city = request.POST.get('city')
        property_obj.description = request.POST.get('description', '')
        property_obj.save()
        messages.success(request, "Property updated successfully")
        return redirect('property_list')
    return render(request, 'rentals/property_form.html', {'property': property_obj})

@login_required
@owner_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, "Property deleted successfully")
        return redirect('property_list')
    return render(request, 'rentals/property_confirm_delete.html', {'property': property_obj})

@login_required
@owner_required
def lease_create(request):
    if request.method == 'POST':
        form = LeaseForm(request.POST, owner=request.user)
        if form.is_valid():
            # The UniqueConstraint in the model handles the "one active lease" rule,
            # but we catch the IntegrityError to provide a friendly message.
            try:
                form.save()
                messages.success(request, "Lease created successfully")
                return redirect('property_list')
            except Exception:
                messages.error(request, "This property already has an active lease.")
                return render(request, 'rentals/lease_form.html', {'form': form})
    else:
        form = LeaseForm(owner=request.user)
    
    return render(request, 'rentals/lease_form.html', {'form': form})

@login_required
@owner_required
def owner_overview(request):
    properties = Property.objects.filter(owner=request.user).prefetch_related('leases')
    # We want to find the active lease for each property
    property_data = []
    for prop in properties:
        active_lease = prop.leases.filter(status='ACTIVE').first()
        property_data.append({
            'property': prop,
            'active_lease': active_lease,
            'tenant': active_lease.tenant if active_lease else None,
            'rent': active_lease.monthly_rent if active_lease else 0,
        })
    
    return render(request, 'rentals/owner_overview.html', {'property_data': property_data})

@login_required
@tenant_required
def tenant_lease_dashboard(request):
    # Get the active lease for the logged-in tenant
    lease = Lease.objects.filter(tenant=request.user, status='ACTIVE').first()
    if not lease:
        messages.error(request, "No active lease found for your account.")
        return redirect('property_list') # Or a suitable landing page
    
    return render(request, 'rentals/tenant_dashboard.html', {'lease': lease})

@login_required
@tenant_required
def payment_submit(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            lease = Lease.objects.filter(tenant=request.user, status='ACTIVE').first()
            if not lease:
                messages.error(request, "You must have an active lease to submit payment.")
                return redirect('tenant_lease_dashboard')
            
            payment = form.save(commit=False)
            payment.lease = lease
            payment.status = Payment.Status.PENDING
            payment.save()
            messages.success(request, "Payment submitted successfully and is pending approval.")
            return redirect('payment_history')
    else:
        form = PaymentForm()
    
    return render(request, 'rentals/payment_form.html', {'form': form})

@login_required
@tenant_required
def payment_history(request):
    # Get all payments for the tenant's leases
    leases = Lease.objects.filter(tenant=request.user)
    payments = Payment.objects.filter(lease__in=leases).order_by('-payment_date')
    return render(request, 'rentals/payment_history.html', {'payments': payments})

@login_required
@owner_required
def payment_approve(request, pk, action):
    payment = get_object_or_404(Payment, pk=pk)
    # Ensure the payment belongs to a property owned by the current user
    if payment.lease.property.owner != request.user:
        raise PermissionDenied
    
    if action == 'approve':
        payment.status = Payment.Status.APPROVED
        messages.success(request, "Payment approved successfully.")
    elif action == 'reject':
        payment.status = Payment.Status.REJECTED
        messages.success(request, "Payment rejected.")
    else:
        messages.error(request, "Invalid action.")
        return redirect('owner_overview')
        
    payment.save()
    return redirect('owner_overview')


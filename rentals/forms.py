from django import forms
from .models import Lease, Property, Payment
from accounts.models import User

class LeaseForm(forms.ModelForm):
    # ...existing code...
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date <= start_date:
            self.add_error('end_date', "End date must be after start date.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        # ...existing code...
        owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        if owner:
            # Only show properties owned by the current owner
            self.fields['property'].queryset = Property.objects.filter(owner=owner)
            # Only show users with the TENANT role
            self.fields['tenant'].queryset = User.objects.filter(role=User.Role.TENANT)

class PaymentForm(forms.ModelForm):
    # ...existing code...
    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount_paid')
        if amount is not None and amount <= 0:
            self.add_error('amount_paid', "Amount paid must be positive.")
        
        lease = cleaned_data.get('lease') # This might be passed in __init__ or provided
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')
        
        if lease and month and year:
            duplicate = Payment.objects.filter(
                lease=lease, 
                month=month, 
                year=year
            ).exclude(pk=self.instance.pk)
            if duplicate.exists():
                self.add_error(None, "A payment for this month and year has already been submitted.")
                
        return cleaned_data

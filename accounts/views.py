from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .decorators import super_admin_required

@login_required
@super_admin_required
def owner_list(request):
    owners = User.objects.filter(role=User.Role.OWNER)
    return render(request, 'accounts/owner_list.html', {'owners': owners})

@login_required
@super_admin_required
def owner_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'accounts/owner_form.html')
            
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password, 
            first_name=first_name, 
            last_name=last_name, 
            role=User.Role.OWNER
        )
        messages.success(request, f"Owner {username} created successfully")
        return redirect('owner_list')
        
    return render(request, 'accounts/owner_form.html')

@login_required
@super_admin_required
def owner_edit(request, pk):
    owner = get_object_or_404(User, pk=pk, role=User.Role.OWNER)
    if request.method == 'POST':
        owner.username = request.POST.get('username')
        owner.email = request.POST.get('email')
        owner.first_name = request.POST.get('first_name')
        owner.last_name = request.POST.get('last_name')
        owner.save()
        messages.success(request, "Owner updated successfully")
        return redirect('owner_list')
    return render(request, 'accounts/owner_form.html', {'owner': owner})

@login_required
@super_admin_required
def owner_delete(request, pk):
    owner = get_object_or_404(User, pk=pk, role=User.Role.OWNER)
    if request.method == 'POST':
        owner.delete()
        messages.success(request, "Owner deleted successfully")
        return redirect('owner_list')
    return render(request, 'accounts/owner_confirm_delete.html', {'owner': owner})


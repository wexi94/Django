from django.shortcuts import render , redirect
from django.contrib import messages , auth
from django.contrib.auth.models import User
from contacts.models import Contacts
def  login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'You are now Logged In')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request , 'accounts/login.html')

def  register(request):
    if request.method == 'POST':
        # Get Form Values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
    # Check If Password Matches
        if password == password2:
        # Check Username
            if User.objects.filter(username=username).exists() :
                messages.error(request , 'That username is Already Taken')
                return redirect('register')
            else :
                if User.objects.filter(email=email).exists() :
                    messages.error(request , 'That Email Is Being Used')
                    return redirect('register')
                else :
                    user = User.objects.create_user(username=username, password=password ,email=email)
                    user.save()
                    messages.success(request, 'You are Now Registered and Can log in ')
                    return redirect('login')
        else :
            messages.error(request , 'Password Do not Match')
            return redirect('register')
    else:
        return render(request , 'accounts/register.html')

def  logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now Logged Out')
        return redirect('index')

def  dashboard(request):
    user_contacts = Contacts.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request , 'accounts/dashboard.html', context)
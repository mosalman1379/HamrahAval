from django.shortcuts import render
from Meeting.forms import SignUpForm, LoginForm, CreateMeetingForm
from django.contrib.auth.models import User
from Meeting.models import MeetingManager, Meeting, Room
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "POST":
        Signup = SignUpForm(data=request.POST)
        if Signup.is_valid():
            cd = Signup.cleaned_data
            user = User.objects.create_user(username=cd['username'], password=cd['password'],
                                            first_name=cd['first_name'], last_name=cd['last_name'])
            user.save()
            if cd['is_manager']:
                manager = MeetingManager.objects.create(user=user, is_manager=True)
                manager.save()
                return render(request, 'meeting/dashboard.html', context={'user': user})
            return render(request, 'meeting/dashboard.html', context={'user': user})
    else:
        form = SignUpForm()
        return render(request, 'meeting/signup.html', {'form': form})


@login_required
def change_status(request):
    assert request.user.is_superuser
    if request.method == "POST":
        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken')
        for key, value in data.items():
            if value[0] == 'on':
                user = User.objects.get(pk=int(key))
                MeetingManager.objects.create(user=user, is_manager=True).save()
        return redirect('Meeting:dashboard')
    else:
        managers_ids = MeetingManager.objects.all().values_list("user_id", flat=True)
        users = User.objects.all().exclude(id__in=managers_ids)
        return render(request, 'meeting/all_users.html', {'users': users})


@login_required
def dashboard(request):
    return render(request, 'meeting/dashboard.html', {'user': request.user})


def login_func(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        cd = form.cleaned_data
        user = authenticate(klass=User, username=cd['username'], password=cd['password'])
        if user:
            login(request, user)
            return render(request, 'meeting/dashboard.html', {'user': user})
        else:
            form = LoginForm()
            return render(request, 'meeting/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'meeting/login.html', {'form': form})


def create_meeting(request):
    rooms = Room.objects.all()
    if request.method == "POST":
        form = CreateMeetingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Meeting.objects.create(room=cd['room'], start_time=cd['start_time'], end_time=cd['end_time'],
                                   duration=cd['duration'], meeting_manager_id=1).save()
            return redirect('Meeting:dashboard')
        else:
            form = CreateMeetingForm()
            return render(request, 'meeting/create_meeting.html', {'form': form, 'rooms': rooms})
    else:
        form = CreateMeetingForm()
        return render(request, 'meeting/create_meeting.html', {'form': form, 'rooms': rooms})

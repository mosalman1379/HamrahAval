from django import forms
from django.contrib.auth.models import User
from Meeting.models import Meeting


class SignUpForm(forms.ModelForm):
    is_manager = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class DateInput(forms.DateTimeInput):
    input_type = 'date'


class CreateMeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].required = False

    class Meta:
        model = Meeting
        fields = ('start_time', 'end_time', 'duration','room')
        widgets = {
            'start_time': DateInput(),
            'end_time': DateInput(),
            'room':forms.HiddenInput
        }

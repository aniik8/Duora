from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import forms, UserCreationForm
class question_form(ModelForm):
    class Meta:
        model = question_data
        fields = ('questions', )

        def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)


class answer_form(ModelForm):
    class Meta:
        model = answer_data
        fields = ['answer']

        def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)


class signupform(UserCreationForm):
    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']


class EditUserinfo(forms.ModelForm):


    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['profile_image', 'bio']


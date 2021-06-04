from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.backends import ModelBackend
from django_enumfield import enum
from django import forms
from main.models import Users


class RegisterForm(forms.ModelForm):
    # email = forms.EmailField(required=True)
    # role = enum.EnumField(Roles)
    name = forms.CharField(
        label='Nazwa użytkownika', min_length=4, max_length=50, help_text='Minimalna liczba znaków: 4', widget=forms.TextInput(attrs={'class': 'form-control form-control'}))
    email = forms.EmailField(max_length=100, error_messages={
        'required': 'Adres email jest wymagany'}, widget=forms.EmailInput(attrs={'class': 'form-control form-control'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-control form-control'}), min_length=8, help_text='Minimalna liczba znaków: 8')
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'class': 'form-control form-control'}))

    class Meta:
        model = Users
        fields = ('name', 'email',)

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        r = Users.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("Taki użytkownik już istnieje")
        return name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError('Podany email jest już zajęty.')
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label='Adres email', max_length=100, error_messages={'required': 'Adres email jest wymagany'}, widget=forms.EmailInput(attrs={'class': 'form-control form-control'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-control form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Users.objects.filter(email__iexact=email)
        if not qs.exists():
            raise forms.ValidationError('Podany adres email nie istnieje')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        email = self.cleaned_data.get('email')
        qs = Users.objects.filter(email__iexact=email)
        if qs.exists():
            user = qs[0]
            if user.check_password(password):
                return password
            raise forms.ValidationError('Hasło jest nieprawidłowe')


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password):
                return user
        return None

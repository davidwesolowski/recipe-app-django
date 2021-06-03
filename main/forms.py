from django import forms
from .models import Users


class CreateRecipeForm(forms.Form):
    title = forms.CharField(label='Tytuł', required=True, max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control'}), label='Opis', max_length=2048, required=True)
    imageUrl = forms.URLField(label='Adres url', required=True, max_length=255, widget=forms.URLInput(attrs={'class': 'form-control form-control'}))


class EditProfile(forms.Form):
    email = forms.EmailField(label='Adres email',
                             widget=forms.EmailInput(attrs={'class': 'form-control form-control', 'readonly': True}), error_messages='')
    name = forms.CharField(
        label='Nazwa użytkownika', widget=forms.TextInput(attrs={'class': 'form-control form-control'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-control form-control'}), required=False)

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        email = self.cleaned_data['email']
        user = Users.objects.get(email=email)
        r = Users.objects.filter(name=name)
        if r.count() and r[0].id != user.id:
            raise forms.ValidationError("Taki użytkownik już istnieje")
        if 0 < len(name) < 4:
            raise forms.ValidationError("Nazwa musi mieć przynajmniej 4 znaki")
        return name

    def clean_password(self):
        password = self.cleaned_data['password']
        if 0 < len(password) < 8:
            raise forms.ValidationError('Hasło musi mieć przynajmniej 8 znaków.')
        return password

'''
class EditProfile(forms.Form):
    email = forms.EmailField(label='Adres email',
                             widget=forms.EmailInput(attrs={'class': 'form-control form-control', 'readonly': True}), error_messages='')
    name = forms.CharField(
        label='Nazwa użytkownika', widget=forms.TextInput(attrs={'class': 'form-control form-control'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-control form-control'}), required=False)

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        r = Users.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("Taki użytkownik już istnieje")
        if 0 < len(name) < 4:
            raise forms.ValidationError("Nazwa musi mieć przynajmniej 4 znaki")
        return name

    def clean_password(self):
        password = self.cleaned_data['password']
        if 0 < len(password) < 8:
            raise forms.ValidationError('Hasło musi mieć przynajmniej 8 znaków.')
        return password
'''
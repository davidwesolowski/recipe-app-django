from django import forms


class CreateRecipeForm(forms.Form):
    title = forms.CharField(label='Tytuł', required=True, max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control'}), label='Opis', max_length=2048, required=True)
    imageUrl = forms.URLField(label='Adres url', required=True, max_length=255, widget=forms.URLInput(attrs={'class': 'form-control form-control'}))

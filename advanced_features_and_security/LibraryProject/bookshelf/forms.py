from django import forms


class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)


class BookSearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=100)

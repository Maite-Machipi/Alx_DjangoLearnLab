from django import forms


class BookSearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=100)

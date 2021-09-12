from django import forms
from django.forms import ModelForm

from .models import Book

from django.db import models


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'publicationDate': forms.DateInput(attrs={'onfocus': "(this.type='date')", 'onblur': "(this.type='text')"})
        }
        labels = {
            'publicationDate': 'Publication Date',
            'image': '',
        }
        exclude = ['isBorrowed']

    def clean(self, *args, **kwargs):
        ISPN = self.cleaned_data.get('ISPN')

        bookExixt = Book.objects.filter(ISPN=ISPN).exists()

        if bookExixt:
            raise forms.ValidationError(
                'The book with this ISPN is already exist !')

        return super(BookForm, self).clean(*args, **kwargs)


class BookUpdateForm(forms.ModelForm):
    currentIspn = forms.CharField(
        disabled=True, label='current ISPN', widget=forms.HiddenInput)

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'publicationDate': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'publicationDate': 'Publication Date',
            'image': '',
        }
        exclude = ['isBorrowed']

    def clean(self, *args, **kwargs):
        oldISPN = self.cleaned_data.get('currentIspn')
        newISPN = self.cleaned_data.get('ISPN')

        booksExcludeCurrentBook = Book.objects.all().exclude(ISPN=oldISPN)
        isNewBookISPNExist = booksExcludeCurrentBook.filter(
            ISPN=newISPN).exists()

        if isNewBookISPNExist:
            raise forms.ValidationError(
                'The book with this ISPN is already exist !')

        return super(BookUpdateForm, self).clean(*args, **kwargs)

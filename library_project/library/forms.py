from django import forms
from .models import Book, Student, IssueBook


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price','cover']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone']


class IssueBookForm(forms.ModelForm):

    class Meta:
        model = IssueBook
        fields = ['student', 'book']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(available=True)
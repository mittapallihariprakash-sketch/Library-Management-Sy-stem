from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import Book, Student, IssueBook
from .forms import BookForm, StudentForm, IssueBookForm
from datetime import date, timedelta


def home(request):
    search = request.GET.get('search')

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book Added Successfully!")
            return redirect('/')

    form = BookForm()

    if search:
        books = Book.objects.filter(title__icontains=search)
    else:
        books = Book.objects.all().order_by('title')

    total_books = Book.objects.count()
    total_students = Student.objects.count()
    issued_books = IssueBook.objects.filter(return_date__isnull=True).count()
    available_books = Book.objects.filter(available=True).count()

    return render(request, 'home.html', {
        'form': form,
        'books': books,
        'total_books': total_books,
        'total_students': total_students,
        'issued_books': issued_books,
        'available_books': available_books,
    })   



def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    messages.success(request, "Book Deleted Successfully!")
    return redirect('/')


def edit_book(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book Updated Successfully!")
            return redirect('/')

    form = BookForm(instance=book)

    return render(request, 'home.html', {
        'form': form,
        'books': Book.objects.all()
    })


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login/')


# Student Registration
def student_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student Registered Successfully!")
            return redirect('/student/')

    else:
        form = StudentForm()

    students = Student.objects.all()

    return render(request, 'student.html', {
        'form': form,
        'students': students
    })

def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)

        if form.is_valid():
    issue = form.save()

    issue.due_date = issue.issue_date + timedelta(days=15)
    issue.save()

    issue.book.available = False
    issue.book.save()

    return redirect('/issue/')

    else:
        form = IssueBookForm()

    issues = IssueBook.objects.all()

    return render(request, 'issue_book.html', {
        'form': form,
        'issues': issues
    })
    

def return_book(request, id):
    issue = IssueBook.objects.get(id=id)

    issue.return_date = date.today()

    days = (issue.return_date - issue.issue_date).days

    if days > 7:
        issue.fine = (days - 7) * 10
    else:
        issue.fine = 0

    issue.book.available = True
    issue.book.save()

    issue.save()
    return redirect('/issue/')
def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('/student/')
def edit_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/student/')
    else:
        form = StudentForm(instance=student)

    students = Student.objects.all()

    return render(request, 'student.html', {
        'form': form,
        'students': students
    })
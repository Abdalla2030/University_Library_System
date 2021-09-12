import json
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import BookForm, BookUpdateForm
from .models import Book, BorrowBook
from registration.models import User

from registration.forms import UserUpdateInfoForm, UserUpdatePassForm
from django.contrib.auth import update_session_auth_hash

from datetime import datetime, timedelta


# Create your views here.


def getUserType(request):
    userQuerySet = User.objects.filter(user=request.user).values()
    userData = [row for row in userQuerySet]
    storedUserType = userData[0]['userType']

    return storedUserType


def isUserTypeValid(request):
    userType = getUserType(request)
    urlParts = str(request.path).split('/')
    urlParts = [val for val in urlParts if val != '']

    neededUrlPart = urlParts[1]

    return userType == neededUrlPart


@login_required(login_url='/')
def adminProfile(request, id):
    if isUserTypeValid(request) == False:
        return redirect('/registration/logout/')

    context = {
        "id": id,
        "name": request.user.get_full_name
    }
    return render(request, 'userProfile/admin/adminProfile.html', context)


@login_required(login_url='/')
def studentProfile(request, id):
    if isUserTypeValid(request) == False:
        return redirect('/registration/logout/')

    context = {
        "id": id,
        "name": request.user.get_full_name
    }
    return render(request, 'userProfile/student/studentProfile.html', context)


@login_required(login_url='/')
def update(request, id, type):
    if isUserTypeValid(request) == False:
        return redirect('/registration/logout/')

    userInstance = request.user

    if type == 'info':
        form = UserUpdateInfoForm(request.POST or None, instance=userInstance)
        if request.method == 'POST':
            if form.is_valid():
                user = form.save(commit=False)
                user.save()

                username = request.user.username
                if id != username:
                    return redirect('/profile/admin/' + username + '/')

                return redirect('/profile/admin/' + id + '/')

    elif type == 'pass':
        form = UserUpdatePassForm(user=userInstance, data=request.POST or None)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            return redirect('/profile/admin/' + id + '/')

    context = {
        'prevPageLink': ('/profile/' + getUserType(request) + '/' + id + '/'),
        'id': id, 'userType': getUserType(request),
        'form': form,
        'type': type
    }

    return render(request, 'userProfile/options/updateUser.html', context)


@login_required(login_url='/')
def addBook(request, id):
    form = BookForm(request.POST or None, request.FILES or None)

    if request.is_ajax():
        if form.is_valid():
            form.save()
            data = {'status': 'ok'}
        else:
            data = json.dumps(
                {'errors': [value for key, value in form.errors.items()]}
            )
            return HttpResponseBadRequest(data)

        return HttpResponse(data)

    context = {
        'prevPageLink': ('/profile/admin/' + id + '/'),
        'form': form
    }

    return render(request, 'userProfile/admin/options/addBook.html', context)


@login_required(login_url='/')
def displayBooks(request, id):
    if isUserTypeValid(request) == False:
        return redirect('/registration/logout/')

    searchKey = str(request.GET.get('searchInput'))
    searchOption = str(request.GET.get('searchOptions'))

    books = Book.objects.all()

    if searchKey.strip() == '':
        books = Book.objects.all()
    else:
        if searchOption == 'name':
            books = Book.objects.filter(name__contains=searchKey)
        elif searchOption == 'ispn':
            books = Book.objects.filter(ISPN__contains=searchKey)
        elif searchOption == 'author':
            books = Book.objects.filter(author__contains=searchKey)
        elif searchOption == 'year':
            books = Book.objects.filter(
                publicationDate__year__contains=searchKey)

    context = {
        'prevPageLink': ('/profile/' + getUserType(request) + '/' + id + '/'),
        'books': books,
        'type': getUserType(request),
        'id': id
    }

    return render(request, 'userProfile/options/showBooks.html', context)


@login_required(login_url='/')
def updateBook(request, id, bookId):
    book = Book.objects.get(ISPN=bookId)
    form = BookUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=book,
        initial={'currentIspn': bookId}
    )

    if request.method == 'POST':
        if form.is_valid():
            newISPN = form.cleaned_data.get('ISPN')

            if newISPN != bookId:
                Book.objects.filter(ISPN=bookId).update(ISPN=newISPN)

            book.save()

            return redirect('/profile/admin/' + id + '/books/')

    context = {
        'prevPageLink': ('/profile/admin/' + id + '/books/'),
        'form': form
    }

    return render(request, 'userProfile/admin/options/updateBook.html', context)


@login_required(login_url='/')
def deleteBook(request, id, bookId):
    book = Book.objects.get(ISPN=bookId)
    book.delete()
    return redirect('/profile/admin/' + id + '/books/')


@login_required(login_url='/')
def borrowBook(request, id, bookId):
    if isUserTypeValid(request) == False:
        return redirect('/registration/logout/')

    if request.method == 'POST':
        borrowingPeriod = int(request.POST.get('borrowingPeriod'))
        book = Book.objects.get(ISPN=bookId)
        user = request.user
        borrowStartDate = datetime.now()
        borrowEndDate = borrowStartDate + timedelta(borrowingPeriod)

        book.isBorrowed = True
        book.save()

        borrowing = BorrowBook.objects.create(
            user=user,
            book=book,
            start_date=borrowStartDate,
            end_date=borrowEndDate,
        )

        borrowing.save()

        return redirect('/profile/' + getUserType(request) + '/' + id + '/books/')

    context = {
        'prevPageLink': ('/profile/' + getUserType(request) + '/' + id + '/books/'),
    }

    return render(request, 'userProfile/options/borrowBook.html', context)


@login_required(login_url='/')
def borrowedBooks(request, id):
    if isUserTypeValid(request) == False:
        return redirect('/registration/logout/')

    searchKey = str(request.GET.get('searchInput'))
    searchOption = str(request.GET.get('searchOptions'))

    books = BorrowBook.objects.filter(user=request.user)

    if searchKey.strip() == '':
        books = BorrowBook.objects.filter(user=request.user)
    else:
        if searchOption == 'name':
            books = BorrowBook.objects.filter(
                user=request.user,
                book__name__contains=searchKey
            )
        elif searchOption == 'ispn':
            books = BorrowBook.objects.filter(
                user=request.user,
                book__ISPN__contains=searchKey
            )
        elif searchOption == 'author':
            books = BorrowBook.objects.filter(
                user=request.user,
                book__author__contains=searchKey
            )
        elif searchOption == 'year':
            books = BorrowBook.objects.filter(
                user=request.user,
                book__publicationDate__year__contains=searchKey
            )

    context = {
        'prevPageLink': ('/profile/' + getUserType(request) + '/' + id + '/'),
        'id': id,
        'type': getUserType(request),
        'books': books
    }
    return render(request, 'userProfile/options/showBorrowedBooks.html', context)


@login_required(login_url='/')
def returnBook(request, id, bookId):
    book = Book.objects.get(ISPN=bookId)
    borrowedBook = BorrowBook.objects.get(book=book, user=request.user)
    borrowedBook.delete()
    book.isBorrowed = False
    book.save()
    return redirect('/profile/' + getUserType(request) + '/' + id + '/borrowed-books/')


@login_required(login_url='/')
def extendingBorrow(request, id, bookId):
    if isUserTypeValid(request) == False:
        return redirect('/registration/logout/')

    if request.method == 'POST':
        extensionPeriod = int(request.POST.get('borrowingPeriod'))
        book = Book.objects.get(ISPN=bookId)
        user = request.user
        borrowing = BorrowBook.objects.get(user=user, book=book)
        borrowing.end_date += timedelta(extensionPeriod)
        borrowing.save()

        return redirect('/profile/' + getUserType(request) + '/' + id + '/borrowed-books/')

    context = {
        'prevPageLink': ('/profile/' + getUserType(request) + '/' + id + '/borrowed-books/'),
    }

    return render(request, 'userProfile/options/extendingBorrowPeriod.html', context)

from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/<str:id>/', include([
        path('', views.adminProfile, name='admin-profile'),
        path('add-book/', views.addBook, name='add-book'),
        path('update/<str:type>', views.update, name='admin-update'),
        path('books/', include([
            path('', views.displayBooks, name='admin-display-books'),
            path('<str:bookId>/borrow', views.borrowBook,
                 name='admin-borrow-book'),
            path('<str:bookId>/update', views.updateBook,
                 name='update-book'),
            path('<str:bookId>/delete', views.deleteBook,
                 name='delete-book')
        ])),
        path('borrowed-books/', include([
            path('', views.borrowedBooks, name='admin-borrowed-books'),
            path('<str:bookId>/return/', views.returnBook,
                 name='admin-return-book'),
            path('<str:bookId>/extending/',
                 views.extendingBorrow, name='admin-extending'),
        ]))
    ])),

    path('student/<str:id>/', include([
        path('', views.studentProfile, name='student-profile'),
        path('update/<str:type>', views.update, name='student-update'),
        path('books/', include([
            path('', views.displayBooks, name='student-display-books'),
            path('<str:bookId>/borrow', views.borrowBook,
                 name='student-borrow-book'),
        ])),
        path('borrowed-books/', include([
            path('', views.borrowedBooks, name='student-borrowed-books'),
            path('<str:bookId>/return/', views.returnBook,
                 name='student-return-book'),
            path('<str:bookId>/extending/',
                 views.extendingBorrow, name='student-extending'),
        ]))
    ])),
]

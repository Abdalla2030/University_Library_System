from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):
    ISPN = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publicationDate = models.DateField()
    image = models.ImageField()
    isBorrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' # ' + self.ISPN


class BorrowBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        unique_together = (('user', 'book'),)

    def __str__(self):
        return self.user.username + '  -->  ' + self.book.ISPN

from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home/home.html')


def admin(request):
    return render(request, 'home/admin.html')


def student(request):
    return render(request, 'home/student.html')

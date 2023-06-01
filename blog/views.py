from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Blog
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html',{'blogs':blogs})

def detail(request,id):
    blog = get_object_or_404(Blog, pk = id)
    return render(request, 'detail.html', {'blog':blog})

def new(request):
    return render(request, 'new.html')

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.writer = request.POST['writer']
    new_blog.body = request.POST['body']
    new_blog.pub_date = timezone.now()
    new_blog.image = request.FILES['image']
    new_blog.save()
    return redirect('detail', new_blog.id)

def edit(request,id):
    edit_blog = Blog.objects.get(id = id)
    return render(request, 'edit.html', {'blog':edit_blog})

def update(request,id):
    update_blog = Blog.objects.get(id = id)
    update_blog.title = request.POST['title']
    update_blog.writer = request.POST['writer']
    update_blog.body = request.POST['body']
    update_blog.pub_date = timezone.now()
    update_blog.save()
    return redirect('detail', update_blog.id)

def delete(request,id):
    delete_blog = Blog.objects.get(id=id)
    delete_blog.delete()
    return redirect('home')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        userid = request.POST['username']
        userpw = request.POST['password']

        user = auth.authenticate(request, username=userid, password=userpw)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        
        else:
            return render(request, 'login.html')
        

def logout(request):
    auth.logout(request)
    return redirect('home')

def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    
    else:
        userid = request.POST['username']
        userpw = request.POST['password']

        new_user = User.objects.create_user(username=userid, password=userpw)

        auth.login(request, new_user)

        return redirect('home')
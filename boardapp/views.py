from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy


def signupfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        #ユーザーの重複を防ぐ処理
        try:
            User.objects.get(username = username2)
            return render(request,"signup.html", {"error":"このユーザーは登録されています。"})
        except:
            user = User.objects.create_user(username2, password2)
            return render(request, 'signup.html', {'some':'somedata'})
    return render(request, 'signup.html', {'some':'somedata'})

def loginfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        user = authenticate(request, username=username2, password=password2)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')
    
#BoardModelの全てのデータを持ってくる
@login_required  
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request,'list.html', {'object_list': object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

def detailfunc(request, pk):
    object = BoardModel.objects.get(pk = pk)
    return render(request,"detail.html", {'object':object}) 

def goodfunc(request, pk):
    post = BoardModel.objects.get(pk = pk)
    post.good += 1
    post.save()
    return redirect('list')

def readfunc(request, pk):
    post = BoardModel.objects.get(pk = pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = post.readtext + ' ' + post2
        post.save()
        return redirect('list')
    
class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'images')
    success_url = reverse_lazy('list')
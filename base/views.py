from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView , UpdateView ,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks') 
    
def signupview(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 and username.isalpha():
            user  = User.objects.create_user(email=email,username=username,password=password1,first_name=first_name)
            user.save()
            return redirect('login')
        else:
            if username.isalpha():
                pass
            else :
                return render(request,'signup.html',{'error_username':'Username should contain only aplhabets'})
            return render(request,'signup.html',{'error':'Passwords do not match'})
   
    return render(request,'signup.html')

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('tasks')
        else:
            return render(request,'login.html',{'error':"Invalid username or password"})
    return render(request,'login.html')

def homePage(request):
    return render(request,"index.html")
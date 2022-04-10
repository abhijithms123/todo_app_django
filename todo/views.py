from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,TemplateView,ListView,DetailView,DeleteView,UpdateView
from todo.forms import UserRegistrationForm,LoginForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login
from todo.models import Todos
from todo.forms import TodoForm,TodoChangeForm

# Create your views here.

class SignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("signin")

class SignINView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})

class UserHome(TemplateView):
    template_name = "userhome.html"

class TodoCreateView(CreateView):
    model = Todos
    form_class = TodoForm
    template_name = "add_todo.html"
    success_url = reverse_lazy("home")

    def post(self,request,*args,**kwargs):
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect("home")
        else:
            return render(request,self.template_name,{"form":form})


class MyTodos(ListView):
    model = Todos
    template_name = "list_todos.html"
    context_object_name = "todos"

    def get_queryset(self):
        qs = Todos.objects.filter(user=self.request.user)
        return qs

    # def get(self,request,*args,**kwargs):
    #     qs = Todos.objects.filter(user=request.user)
    #     return render(request,self.template_name,{"todos":qs})

class TodoDetail(DetailView):
    model = Todos
    template_name = "todo_detail.html"
    context_object_name = "todo"
    pk_url_kwarg = "id"

class EditTodo(UpdateView):
    model = Todos
    form_class = TodoChangeForm
    template_name = "edit_todo.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("alltodos")


def remove_todo(request,id):
    todo = Todos.objects.get(id=id)
    todo.delete()
    return redirect("alltodos")


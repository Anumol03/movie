from django.shortcuts import render,redirect
from django.views.generic import View,FormView
from myapp.forms import RegistrationForm,LoginForm,MovieForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from myapp.models import Movie
from django.utils.decorators import method_decorator
def sign_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"you must login")
            return redirect("signin")
        return fn(request,*args,**kwargs)
    return wrapper
class SignUpView(View):
  
    model=User
    template_name="register.html"
    form_class=RegistrationForm
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"account has been created")
            return redirect("signin")
        messages.error(request,"failed to create account")
        return render(request,self.template_name,{"form":form})

class SignInView(View):
    model=User
    template_name="login.html"
    form_class=LoginForm
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
            messages.error(request,"login error")
            return render(request,self.template_name,{"form":form})
@method_decorator(sign_required,name="dispatch")
class IndexView(View):
    template_name="index.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
@method_decorator(sign_required,name="dispatch")
class MovieCreateView(View):
    model=Movie
    form_class=MovieForm
    template_name="movie-add.html"
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(files=request.FILES,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"create movie successfully")
            return redirect("movie-list")
        messages.error(request,"failed to create movie")
        return render(request,self.template_name,{"form":form})
@method_decorator(sign_required,name="dispatch")
class MovieListView(View):
    model=Movie
    template_name="movie-list.html"
    def get(self,request,*args,**kwargs):
        qs=Movie.objects.all()
        return render(request,self.template_name,{"movies":qs})
@method_decorator(sign_required,name="dispatch")
class MovieDetailView(View):
    model=Movie
    template_name="movie-detail.html"
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Movie.objects.get(id=id)
        return render(request,self.template_name,{"movies":qs})
@method_decorator(sign_required,name="dispatch")
class MovieEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Movie.objects.get(id=id)
        form=MovieForm(instance=obj)
        return render(request,"movie-edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Movie.objects.get(id=id)
        form=MovieForm(instance=obj,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"changed successfully")
            return redirect("movie-detail",pk=id)
        messages.error(request,"not changed")
        return render(request,"movie-edit.html",{"form":form})
@sign_required
def movie_delet_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    Movie.objects.get(id=id).delete()
    messages.success(request,"movie removed")
    return redirect("movie-list")
def sign_out_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")
class PasswordResetView(FormView):
    model=User
    template_name="password-reset.html"
    form_class=PasswordResetForm
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pwd1=form.cleaned_data.get("password1")
            pwd2=form.cleaned_data.get("password2")
            if pwd1==pwd2:
                try:
                    usr=User.objects.get(username=username,email=email)
                    
                    usr.set_password(pwd1)
                    usr.save()
                    messages.success(request,"password changed")
                    return redirect("signin")
                except Exception as e:
                    messages.error(request,"invalid ctredentials")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request,"password mismatch")
                return render(request,self.template_name,{"form":form})
    

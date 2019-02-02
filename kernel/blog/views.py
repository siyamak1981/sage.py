
from django.views.generic import ListView, DetailView, TemplateView


class PostListView(TemplateView):
   
    template_name = 'mysite/about.html'
   

class HomeView(TemplateView):
 
    template_name = 'mysite/index.html'
    

class PrductListView(TemplateView):
    template_name = 'mysite/product.html'
    page_name = 'product_new'


class SignupListView(TemplateView):
    template_name = 'mysite/signup.html'
    page_name = 'signup'

class SignoutListView(TemplateView):
    template_name = 'mysite/signout.html'
    page_name = 'signout'

class SigninListView(TemplateView):
    template_name = 'mysite/signin.html'
    page_name = 'signin'
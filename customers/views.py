from typing import Any
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic 
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Customer,Agent,Category
from .forms import CustomerForm, CustomerModelForm,CustomUserCreationForm,AssignAgentForm,CustomerCategoryUpdateForm
# Create your views here.

class SignupView(generic.CreateView):
     template_name = "registration/signup.html"
     form_class = CustomUserCreationForm

     def get_success_url(self):
          return reverse("login")

class LandingPageView(generic.TemplateView):
     template_name = "landing.html"

def landing_page(request):
     return render(request,"landing.html" )

class CustomerListView(LoginRequiredMixin,generic.ListView):
     template_name = "customers/customer_list.html"
     context_object_name = "customers"

     def get_queryset(self):
          user = self.request.user
          #Initial queryset of customers for the entire organisation
          if user.is_organisor:
            queryset = Customer.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
          else:
            queryset = Customer.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
          return queryset
     def get_context_data(self, **kwargs) :
         context = super(CustomerListView,self).get_context_data(**kwargs)
         user = self.request.user
         if user.is_organisor:
            queryset = Customer.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_customers": queryset
            })
         return context

def customer_list(request):
    customers = Customer.objects.all()
    context = {
        "customers": customers
    }
    #return HttpResponse("Hello world")
    return render(request,"customers/customer_detail.html", context)

class CustomerDetailView(LoginRequiredMixin,generic.DetailView):
     template_name = "customers/customer_detail.html"
     context_object_name = "customer"

     def get_queryset(self):
          user = self.request.user
          #Initial queryset of customers for the entire organisation
          if user.is_organisor:
            queryset = Customer.objects.filter(organisation=user.userprofile)
          else:
            queryset = Customer.objects.filter(organisation=user.agent.organisation)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
          return queryset


def customer_detail(request,pk):
    customer = Customer.objects.get(id=pk)
    context = {
        "customer": customer
    }
    return render(request,"customers/customer_detail.html", context)

class CustomerCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
     template_name = "customers/customer_create.html"
     form_class = CustomerModelForm

     def get_success_url(self):
          return reverse("customers:customer-list")
     
     def form_valid(self, form):
          customer = form.save(commit=False)
          customer.organisation = self.request.user.userprofile
          customer.save()
          # TODO send email
          send_mail(
               subject="A lead has been created",
               message="Go to the site to see the new lead",
               from_email = "test@test.com",
               recipient_list=["test2@test.com"]
          )
          return super(CustomerCreateView, self).form_valid(form)
     
def customer_create(request):
    form = CustomerModelForm()
    if request.method == "POST":
        print('Receiving a post request')
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/customers")
    context = {
        "form" : form
    }
    return render(request,"customers/customer_create.html",context)

class CustomerUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
     template_name = "customers/customer_update.html"
     form_class = CustomerModelForm

     def get_queryset(self):
          user = self.request.user
          #Initial queryset of customers for the entire organisation
          return Customer.objects.filter(organisation=user.userprofile)

     def get_success_url(self):
          return reverse("customers:customer-list")
     
     

def customer_update(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerModelForm(instance=customer)
    form = CustomerModelForm(request.POST, instance=customer)
    if form.is_valid():
            form.save()
            return redirect("/customers")
    context = {
         "form" : form,
         "customer": customer
     }
    return render(request, "customers/customer_update.html",context)

class CustomerDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
     template_name = "customers/customer_delete.html"

     def get_success_url(self):
          return reverse("customers:customer-list")
     
     def get_queryset(self):
          user = self.request.user
          #Initial queryset of customers for the entire organisation
          return Customer.objects.filter(organisation=user.userprofile)

def customer_delete(request, pk):
     customer = Customer.objects.get(id=pk)
     customer.delete()
     return redirect("/customers")

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "customers/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("customers:customer-list")
    
    def form_valid(self,form):
        agent = form.cleaned_data["agent"]
        customer = Customer.objects.get(id=self.kwargs["pk"])
        customer.agent = agent
        customer.save()
        return super(AssignAgentView,self).form_valid(form)
    
class CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name = "customers/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Customer.objects.filter(
                organisation=user.userprofile,
            )
        else:
            queryset = Customer.objects.filter(organisation=user.agent.organisation) 
        context.update({
            "unassigned_customer_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
          user = self.request.user
          #Initial queryset of customers for the entire organisation
          if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile,
            )
          else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
            
          return queryset
    
class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "customers/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)

    #     customers = self.get_object().customers.all()

    #     context.update({
    #         "customers": customers
    #     })
    #     return context

    def get_queryset(self):
          user = self.request.user
          #Initial queryset of customers for the entire organisation
          if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile,
            )
          else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
            
          return queryset

class CustomerCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "customers/customer_category_update.html"
    form_class = CustomerCategoryUpdateForm

    def get_queryset(self):
          user = self.request.user
          #Initial queryset of customers for the entire organisation
          if user.is_organisor:
            queryset = Customer.objects.filter(
                organisation=user.userprofile,
            )
          else:
            queryset = Customer.objects.filter(organisation=user.agent.organisation)
            queryset  =queryset.filter(agent__user=user)
            
          return queryset

    def get_success_url(self):
          return reverse("customers:customer-detail", kwargs={"pk": self.get_object().id})

# def customer_update(request,pk):
#     customer = Customer.objects.get(id=pk)
#     form = CustomerForm()
#     if request.method == "POST":
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             customer.first_name = first_name
#             customer.last_name = last_name
#             customer.age = age
#             customer.save()
#             return redirect("/customers")
#     context = {
#         "form" : form,
#         "customer": customer
#     }
#     return render(request, "customers/customer_update.html",context)

# def customer_create(request):
    # form = CustomerForm()
    # if request.method == "POST":
    #     print('Receiving a post request')
    #     form = CustomerForm(request.POST)
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         Customer.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         return redirect("/customers")
    # context = {
    #     "form" : form
    # }
#     return render(request,"customers/customer_create.html",context)
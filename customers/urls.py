from django.urls import path
from .views import (CustomerListView,CustomerCategoryUpdateView,
                    CustomerDetailView,CustomerCreateView,CustomerUpdateView,
                    CustomerDeleteView,AssignAgentView,CategoryListView,CategoryDetailView
)
app_name = "customers"

urlpatterns = [
    path('', CustomerListView.as_view() , name='customer-list'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('<int:pk>/update', CustomerUpdateView.as_view(), name='customer-update'),
    path('<int:pk>/delete', CustomerDeleteView.as_view(), name='customer-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'), 
    path('<int:pk>/category/', CustomerCategoryUpdateView.as_view(), name='customer-category-update'),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    path('create/', CustomerCreateView.as_view(), name='customer-create'), 
    path('categories/',CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/',CategoryDetailView.as_view(), name='category-detail')
]
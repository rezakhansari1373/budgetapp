from django.urls import path

from . import views

urlpatterns = [
    path('sw.js', views.service_worker, name='service_worker'),
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/export/', views.export_transactions, name='transaction_export'),
    path('transactions/add/', views.transaction_add, name='transaction_add'),
    path('transactions/<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.budget_add, name='budget_add'),
    path('budgets/<int:pk>/edit/', views.budget_edit, name='budget_edit'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    path('recurring/', views.recurring_list, name='recurring_list'),
    path('recurring/add/', views.recurring_add, name='recurring_add'),
    path('recurring/<int:pk>/edit/', views.recurring_edit, name='recurring_edit'),
    path('recurring/<int:pk>/toggle/', views.recurring_toggle, name='recurring_toggle'),
    path('recurring/<int:pk>/delete/', views.recurring_delete, name='recurring_delete'),
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/add/', views.goal_add, name='goal_add'),
    path('goals/<int:pk>/deposit/', views.goal_deposit, name='goal_deposit'),
    path('goals/<int:pk>/edit/', views.goal_edit, name='goal_edit'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
]

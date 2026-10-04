"""
URL patterns for HOOVALE products app
Phase 1: SEO Foundation
"""
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Products
    path('products/', views.products_list, name='products_list'),
    path('categories/', views.categories_index, name='categories_index'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('collection/<slug:slug>/', views.banner_page, name='banner_page'),

    # CITY LANDING PAGES (Programmatic SEO — high priority)
    path('locations/', views.cities_index, name='cities_index'),
    path('wall-clock-supplier-in-<slug:slug>/', views.city_landing, name='city_landing'),

    # INDUSTRY PAGES
    path('industries/', views.industries_index, name='industries_index'),
    path('wall-clocks-for-<slug:slug>/', views.industry_page, name='industry_page'),

    # SERVICE PAGES
    path('services/', views.services_index, name='services_index'),
    path('services/<slug:slug>/', views.service_page, name='service_page'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    # Static
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Enquiry
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),

    # Robots
    path('robots.txt', views.robots_txt, name='robots'),
]

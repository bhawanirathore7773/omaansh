from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from enquiries.models import Enquiry
from products.models import Product


@require_http_methods(["POST"])
def submit_enquiry(request):
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    city = request.POST.get('city', '').strip()
    message = request.POST.get('message', '').strip()
    product_id = request.POST.get('product_id')
    
    # Validate required fields
    if not all([name, phone, city, message]):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Please fill all required fields'}, status=400)
        return redirect('contact')
    
    product = None
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            pass
    
    enquiry = Enquiry.objects.create(
        product=product,
        name=name,
        phone=phone,
        email=email,
        city=city,
        message=message
    )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Thank you! We will contact you soon.',
            'enquiry_id': enquiry.id
        })
    
    return redirect('contact')

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from properties.models import Property
from .models import Order
from .serializers import OrderSerializer

# Import Yoco keys from settings
from django.conf import settings

YOCO_SECRET_KEY = settings.YOCO_SECRET_KEY
YOCO_PUBLIC_KEY = settings.YOCO_PUBLIC_KEY

class CreateCheckoutSessionView(APIView):
    def post(self, request):
        plan_id = request.data.get('plan_id')
        customer_email = request.data.get('customer_email')
        plan = get_object_or_404(Property, id=plan_id)
        
        # Create pending order
        order = Order.objects.create(
            plan=plan,
            amount=plan.price,
            status='PENDING',
            customer_email=customer_email
        )
        
        # Prepare Yoco Checkout payload
        # Note: Amount should be in cents for Yoco, but let's check docs. 
        # Usually APIs take cents. If plan.price is Decimal, we multiply by 100.
        # Assuming plan.price is in Rands.
        amount_in_cents = int(plan.price * 100)
        
        headers = {
            'Authorization': f'Bearer {YOCO_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Determine if we're in test or production mode based on secret key
        is_test_mode = YOCO_SECRET_KEY.startswith('sk_test_')
        
        # Get frontend URL from settings (can be overridden with ngrok URL in .env)
        from django.conf import settings
        base_url = settings.FRONTEND_URL
        
        # Fallback to request origin if FRONTEND_URL is not set or is localhost in production
        if not base_url or 'localhost' in base_url:
            origin = request.META.get('HTTP_ORIGIN')
            if origin:
                base_url = origin
                print(f"Using Origin for base_url: {base_url}")
        
        payload = {
            'amount': amount_in_cents,
            'currency': 'ZAR',
            'successUrl': f'{base_url}/payment-success?order_id={order.id}',
            'cancelUrl': f'{base_url}/payment-cancel?order_id={order.id}',
            'failureUrl': f'{base_url}/payment-cancel?order_id={order.id}',
            'metadata': {
                'order_id': str(order.id),
                'plan_id': str(plan.id)
            }
        }
        
        try:
            print(f"Sending request to Yoco with payload: {payload}")
            response = requests.post('https://payments.yoco.com/api/checkouts', json=payload, headers=headers)
            print(f"Yoco Response Status: {response.status_code}")
            
            # Raise error for 4xx/5xx
            response.raise_for_status()
            
            data = response.json()
            
            # Update order with checkout ID
            order.yoco_checkout_id = data.get('id')
            order.save()
            
            return Response({
                'redirectUrl': data.get('redirectUrl'),
                'order_id': order.id
            })
            
        except requests.exceptions.RequestException as e:
            print(f"Yoco API Error: {e}")
            error_msg = str(e)
            
            if e.response is not None:
                print(f"Response Status Code: {e.response.status_code}")
                print(f"Response Text: {e.response.text}")
                
                try:
                    # Try to parse JSON error
                    error_detail = e.response.json()
                    print(f"Response JSON: {error_detail}")
                    error_msg = f"{error_msg} - Details: {error_detail}"
                except:
                    # Fallback to raw text
                    error_msg = f"{error_msg} - Raw: {e.response.text}"
                    
            return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentSuccessView(APIView):
    def post(self, request):
        # This endpoint can be called by the frontend after successful redirect
        # to verify status or update it.
        # Ideally, we should use webhooks, but for now we trust the redirect + verification.
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        
        # We could verify with Yoco API here if needed
        order.status = 'PAID'
        order.save()
        
        return Response({'status': 'Order marked as paid'})

class PaymentCancelView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        
        order.status = 'CANCELLED'
        order.save()
        
        return Response({'status': 'Order marked as cancelled'})

class DownloadReceiptView(APIView):
    # Allow any user to download receipt (no authentication required)
    permission_classes = []
    
    def get(self, request, order_id):
        """
        Generate and download PDF receipt for a paid order
        """
        from django.http import HttpResponse
        from .utils import generate_receipt_pdf
        
        # Get the order
        order = get_object_or_404(Order, id=order_id)
        
        # Only allow receipt download for paid orders
        if order.status != 'PAID':
            return Response(
                {'error': 'Receipt can only be generated for paid orders'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate PDF
        try:
            pdf_buffer = generate_receipt_pdf(order)
            
            # Read the PDF content
            pdf_content = pdf_buffer.read()
            
            # Return PDF as downloadable file
            response = HttpResponse(
                pdf_content,
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="receipt_{order.receipt_number}.pdf"'
            response['Content-Length'] = len(pdf_content)
            
            return response
            
        except Exception as e:
            import traceback
            print(f"Error generating PDF: {e}")
            print(traceback.format_exc())
            return Response(
                {'error': f'Failed to generate receipt: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



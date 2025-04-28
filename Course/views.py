from django.shortcuts import render,reverse
from .models import Course,Coupon,CoursePurchase,SiteSettings
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import uuid
from django.views.decorators.csrf import csrf_exempt

from sslcommerz_lib import SSLCOMMERZ
import requests

# Create your views here.
def all_courses(request):
    courses = Course.objects.all()
    return render(request, 'Courses/all_courses.html', {'courses': courses})

def course_details(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'Courses/course_details.html', {'course': course})



@login_required(login_url='login')
def checkout(request, id):
    course = get_object_or_404(Course, id=id)

    # ❌ Prevent duplicate purchases
    already_purchased = CoursePurchase.objects.filter(
        user=request.user,
        course=course,
        is_ordered=True
    ).exists()

    if already_purchased:
        messages.error(request, "You have already purchased this course.")


    total_price = course.price
    discount_amount = Decimal('0.00')
    coupon_code = None
    applied_coupon = False

    # Handle coupon application
    if request.method == 'POST':
        # Apply coupon
        if 'coupon_code' in request.POST:
            code = request.POST.get('coupon_code').strip()
            try:
                coupon = Coupon.objects.get(title__iexact=code, is_expired=False)
                now = timezone.now()

                if coupon.start_date_time and coupon.start_date_time > now:
                    messages.error(request, "Coupon is not yet valid.")
                    return redirect('checkout', id=course.id)
                elif coupon.end_date_time and coupon.end_date_time < now:
                    coupon.is_expired = True
                    coupon.save()
                    messages.error(request, "Coupon has expired.")
                    return redirect('checkout', id=course.id)
                elif coupon.minimum_amount and course.price < coupon.minimum_amount:
                    messages.error(request, f"Coupon valid for purchases over ৳{coupon.minimum_amount}")
                    return redirect('checkout', id=course.id)
                elif request.user in coupon.used_by.all():
                    messages.error(request, "You have already used this coupon.")
                    return redirect('checkout', id=course.id)
                else:
                    discount_amount = coupon.discount
                    total_price -= discount_amount
                    coupon_code = code
                    applied_coupon = True

                    request.session['coupon_code'] = coupon_code
                    request.session['discounted_price'] = str(total_price)
                    request.session['applied_coupon'] = True

                    messages.success(request, f"Coupon '{coupon_code}' applied successfully! You saved ৳{discount_amount}")

            except Coupon.DoesNotExist:
                messages.error(request, "Invalid or expired coupon.")
                return redirect(request.META.get('HTTP_REFERER', 'checkout'))

        # Handle payment submission
        elif 'payment_submit' in request.POST:
            tran_id = uuid.uuid4()
            payment_method = request.POST.get('payment_method', 'ssl')

            discounted_price = Decimal(request.session.get('discounted_price', total_price))
            coupon_code = request.session.get('coupon_code', None)

            purchase = CoursePurchase.objects.create(
                user=request.user,
                course=course,
                amount_paid=discounted_price,
                coupon_applied=coupon_code,
                tran_id=tran_id,
                is_ordered=(payment_method != 'ssl')
            )

            request.session.pop('coupon_code', None)
            request.session.pop('discounted_price', None)
            request.session.pop('applied_coupon', None)

            if payment_method == 'ssl':
                ssl_url = reverse('sslcommerz') + f'?tran_id={tran_id}'
                return redirect(ssl_url)
            else:
                messages.success(request, "Course purchased successfully!")
                return redirect('course-detail', id=course.id)

    context = {
        'course': course,
        'discount_amount': discount_amount,
        'total_price': total_price,
        'coupon_code': coupon_code,
        'applied_coupon': applied_coupon,
        'already_purchased': already_purchased
    }
    return render(request, 'Courses/checkout.html', context)






@login_required(login_url='login')
def sslcommerz(request):
    tran_id = request.GET.get('tran_id')
    total_price = Decimal(request.GET.get('total_price', '0.00'))
    user = request.user

    try:
        purchase = CoursePurchase.objects.get(tran_id=tran_id)
        total = purchase.amount_paid
        course_title = purchase.course.title
        category_name = purchase.course.category.name if purchase.course.category else 'Course'
    except CoursePurchase.DoesNotExist:
        messages.warning(request, "Purchase not found.")
        return redirect('checkout', id=purchase.course.id)

    # Domain
    current_domain = request.build_absolute_uri('/')[:-1].strip("/")

    # Site SSL config
    site_settings = SiteSettings.objects.first()
    if not site_settings:
        messages.warning(request, "Site settings not configured.")
        return redirect('checkout', id=purchase.course.id)


    ssl_config = site_settings.get_ssl_config()
    sslcz = SSLCOMMERZ({
        'store_id': ssl_config['store_id'],
        'store_pass': ssl_config['store_pass'],
        'issandbox': ssl_config['issandbox'],
    })

    # Build request payload
    data = {
        'total_amount': total,
        'currency': "BDT",
        'tran_id': str(tran_id),
        'success_url': f"{current_domain}/Course/success/",
        'fail_url': f"{current_domain}/Course/fail/",
        'emi_option': "0",
        'cus_name': f"{user.first_name or user.username} {user.last_name or ''}",
        'cus_email': user.email,
        'cus_phone': "01700000000",
        'cus_add1': "N/A",
        'cus_city': "N/A",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'num_of_item': 1,
        'product_name': course_title,
        'product_category': category_name,
        'product_profile': "digital",
        'value_a': f'{user.id}'
    }

    response = sslcz.createSession(data)

    if 'GatewayPageURL' in response:
        return redirect(response['GatewayPageURL'])
    else:
        messages.warning(request, "Payment session creation failed. Please try again.")
        return redirect('checkout', id=purchase.course.id)



@csrf_exempt
def success(request):
    if request.method == 'POST':
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            messages.warning(request, "Site settings not configured.")
            return redirect('home')

        ssl_config = site_settings.get_ssl_config()
        sslcz = SSLCOMMERZ({
            'store_id': ssl_config['store_id'],
            'store_pass': ssl_config['store_pass'],
            'issandbox': ssl_config['issandbox']
        })

        post_data = request.POST
        tran_id = post_data.get('tran_id')

        if not tran_id:
            messages.error(request, "Transaction ID is missing.")
            return redirect('home')

        try:
            purchase = CoursePurchase.objects.get(tran_id=tran_id)
        except CoursePurchase.DoesNotExist:
            messages.warning(request, "Purchase not found.")
            return redirect('home')

        course = purchase.course

        response = sslcz.transaction_query_tranid(tran_id)

        if response['element'][0]['status'] == 'VALID':
            user_id = response['element'][0].get('value_a')

            if not user_id:
                messages.error(request, "User information missing in payment data.")
                return redirect('home')

            # Mark purchase as completed
            purchase.is_ordered = True
            purchase.save()

            # Mark coupon as used
            if purchase.coupon_applied:
                try:
                    coupon = Coupon.objects.get(title=purchase.coupon_applied)
                    coupon.used_by.add(purchase.user)
                    coupon.save()
                except Coupon.DoesNotExist:
                    pass

            # Clear coupon data from session
            request.session.pop('coupon_code', None)
            request.session.pop('discounted_price', None)
            request.session.pop('applied_coupon', None)

            messages.success(request, "Your course purchase was successful! You can now access the course.")

            context = {
                'course': course,
                'order': purchase,
                'val_id': post_data.get('val_id'),
                'tran_id': tran_id,
                'amount': post_data.get('amount'),
                'card_type': post_data.get('card_type'),
                'store_amount': post_data.get('store_amount'),
                'card_no': post_data.get('card_no'),
                'bank_tran_id': post_data.get('bank_tran_id'),
                'currency': post_data.get('currency'),
                'risk_title': post_data.get('risk_title'),
                'risk_level': post_data.get('risk_level'),
            }
            return render(request, 'SSL/success.html', context)

        else:
            messages.error(request, "Invalid transaction status from gateway.")
            return redirect('course-detail', id=purchase.course.id)

    return redirect('home')






@csrf_exempt
def fail(request):
    return render(request, 'SSL/fail.html')

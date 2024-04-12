from django.shortcuts import render, redirect
from store_app.models import Product, Categories, Filter_Price, Color, Brand, Contact_us,Order,OrderItem
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import paypalrestsdk
from django.urls import reverse
from routersale.forms import OrderForm
from routersale.utils.invoice import send_invoice



def BASE(request):
    return render(request, 'Main/base.html')

def HOME(request):
    product = Product.objects.all()
    context = {
        'product':product
    }
    return render(request, 'Main/index.html', context)

def PRODUCT(request):
    categories = Categories.objects.all()
    product = Product.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLORID = request.GET.get('color')
    BRANDID = request.GET.get('brand')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    PRICE_LOWTOHIGHID = request.GET.get('LOWTOHIGH')
    PRICE_HIGHTOLOWID = request.GET.get('HIGHTOLOWID')
    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')


    if CATID:
        product = Product.objects.filter(categories=CATID, status='Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price=PRICE_FILTER_ID, status='Publish')
    elif COLORID:
        product = Product.objects.filter(color=COLORID, status='Publish')
    elif BRANDID:
        product = Product.objects.filter(brand=BRANDID, status='Publish')
    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='Old').order_by('id')
    else:
        product = Product.objects.filter(status='Publish').order_by('-id')
        

    context = {
        'product':product,
        'categories':categories,
        'filter_price':filter_price,
        'color':color,
        'brand':brand,
    }
    return render(request, 'Main/product.html', context)

def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = query)
    context = {
        'product': product
    }
    return render(request, 'Main/search.html', context)

def PRODUCT_DETAIL_PAGE(request, id):
    prod = Product.objects.filter(id = id).first()
    context = {
        'prod': prod
    }
    return render(request, 'Main/product_single.html', context)

def CONTACT_PAGE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        

        contact = Contact_us(
        name = name,
        email = email,
        subject = subject,
        message = message,
        )
        
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER

        
        send_mail(subject, message, email_from, ['Tharsan@routersale.com'])
        contact.save()
        return redirect('home')
    #except:
           # return redirect('contact')
    
    return render(request, 'Main/contact.html')

def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2= request.POST.get('pass2')

        customer = User.objects.create_user(username, email, pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')
    return render(request, 'Registration/auth.html')
    
def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')


    return render(request, 'Registration/auth.html')

def HandleLogout(request):
    logout(request)
    return redirect('home')



@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


def Check_out(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            order = form.save(commit=False)  # Save the form data to create an Order instance
            uid = request.session.get('_auth_user_id')
            user = User.objects.get(id = uid)
            # add user data
            order.user = user
            order.save()  # Save the order to get its ID
         
            # Access the cart
            cart = Cart(request)
            # Iterate over items in the cart and create OrderItem instances
            for item in cart.cart.values():
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                price = item['price']
                total = int(item['price']) * item['quantity']

                order_item = OrderItem(
                    order=order,
                    product=product.name,
                    product_id=product,
                    image=product.image,
                    quantity=quantity,
                    price=price,
                    total=total
                )
                order_item.save()
            return render(request, 'Cart/placeorder.html', {'order_id': order.id})
    else:
        form = OrderForm()
    
    return render(request, 'Cart/checkout.html', {'form': form})

# ! No longer in use, handled by Checkout_view
def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        
        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            city = city,
            address = address,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount,
        )
        order.save()
        
        # Access the cart
        cart = Cart(request)
        # Iterate over items in the cart and create OrderItem instances
        for item in cart.cart.values():
            product = Product.objects.get(id=item['product_id'])
            quantity = item['quantity']
            price = item['price']
            total = int(item['price']) * item['quantity']

            order_item = OrderItem(
                order=order,
                product=product.name,
                product_id=product,
                image=product.image,
                quantity=quantity,
                price=price,
                total=total
            )
            order_item.save()

    return render(request, 'Cart/placeorder.html')


paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def create_payment(request, order_id):
    order = Order.objects.get(id=order_id)    
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment', kwargs={'order_id': order_id})),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": order.amount.replace('$', ''),  # Total amount in USD, `$` mark removed
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'paypal_gateway/payment_failed.html')
    

def execute_payment(request, order_id):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment successful, update your Order model
        order = Order.objects.get(id=order_id)  # Retrieve the associated Order object
        order.payment_id = payment_id
        order.payer_id = payer_id
        order.paid = True
        order.save()  # Save the updated Order object
        
         # Iterate over order items and deduct quantities from product's available units
        for order_item in order.orderitem_set.all():
            product = order_item.product_id # product obj
            quantity = order_item.quantity
            
            # Deduct quantity from available units
            product.number_of_available_units -= int(quantity)
            product.save()  # Save the updated product
        
        # Access the cart
        cart = Cart(request)
        # Clear the cart (if needed)
        cart.clear()
        
         # Prepare items for the invoice
        invoice_items = order.orderitem_set.all()
         # Send the invoice
        invoice_response = send_invoice(settings.MERCHANT_EMAIL, order.email, order, invoice_items)  # Assuming email is stored in the order object
        if invoice_response:
            # Invoice sent successfully
            print("Invoice sent successfully", invoice_response)
        else:
            # Invoice sending failed
            print("Failed to send invoice")
        
        return render(request, 'paypal_gateway/payment_success.html')
    else:
        return redirect('payment_failed')
    
def payment_failed(request):
    return render(request, 'paypal_gateway/payment_failed.html')

def payment_checkout(request):
    return render(request, 'paypal_gateway/checkout.html')


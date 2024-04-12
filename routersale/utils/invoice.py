from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from threading import Thread

def send_email(subject, from_email, to_email, html_template, context):
    # Create HTML content for the email using a Django template
    html_content = render_to_string(html_template, context)

    # Create text content by stripping HTML tags
    text_content = strip_tags(html_content)

    # Create the email message
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to_email],
    )
    # Attach HTML content
    msg.attach_alternative(html_content, "text/html")

    try:
        # Send the email
        msg.send()
        return True
    except Exception as e:
        # Handle any exceptions
        print(f"Error sending email: {e}")
        return False

def send_invoice(merchant_email, customer_email, order, items=[]):
    # Send payment confirmation email to the customer
    customer_subject = 'Payment Confirmation'
    customer_template = 'email/payment_confirmation.html'
    customer_context = {'items': items, 'order': order}

    # Send new order received email to the merchant
    merchant_subject = 'New Order Received'
    merchant_template = 'email/new_order_received.html'
    merchant_context = {'order': order}

    # Define functions to send emails
    def send_customer_email():
        send_email(customer_subject, merchant_email, customer_email, customer_template, customer_context)

    def send_merchant_email():
        send_email(merchant_subject, merchant_email, merchant_email, merchant_template, merchant_context)

    # Create threads to send emails in parallel
    customer_thread = Thread(target=send_customer_email)
    merchant_thread = Thread(target=send_merchant_email)

    # Start both threads
    customer_thread.start()
    merchant_thread.start()

    # Wait for both threads to finish
    customer_thread.join()
    merchant_thread.join()

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.utils import timezone
from customers.models import Customer
import pytz

logger = get_task_logger(__name__)


@shared_task(name="customers.tasks.send_birthday_wishes")
def send_birthday_wishes():
    now_utc = timezone.now()

    current_date_utc = now_utc.date()

    customers_with_birthday = Customer.objects.filter(
        birthdate__day=current_date_utc.day,
        birthdate__month=current_date_utc.month,
    )

    for customer in customers_with_birthday:
        customer_tz = pytz.timezone(customer.timezone)
        customer_local_time = now_utc.astimezone(customer_tz)

        # ignore if customers tz is behind the server
        if customer_local_time < now_utc:
            continue

        # Calculate the time until 11:59 PM in the customer's timezone
        hours_until_wish = 23 - customer_local_time.hour
        minutes_until_wish = 59 - customer_local_time.minute

        # Calculate the total delay in seconds
        delay_seconds = hours_until_wish * 3600 + minutes_until_wish * 60

        # Delay the task for the appropriate time
        send_birthday_wishes_to_customer.apply_async(
            (customer.id,), countdown=delay_seconds
        )


@shared_task(name="customers.tasks.send_birthday_wishes_to_customer")
def send_birthday_wishes_to_customer(customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        subject = "Happy Birthday!"
        message = f"Dear {customer.user.username},\n\nWishing you a fantastic birthday!"
        from_email = "your_email@example.com"
        recipient_list = [customer.user.email]
        print(f" email should be sent to {recipient_list} with subject: {subject}")
        #send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Sent birthday wishes to {customer.name} via email.")

    except Customer.DoesNotExist:
        logger.error(f"Customer with ID {customer_id} not found.")

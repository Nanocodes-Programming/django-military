from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import random

def send_template_email(template, email, subject, **context):
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        "MS Network <{}>".format(settings.EMAIL_HOST_USER),
        [email],
        #this is example
        html_message=html_message,
    )
    
    
def get_expiration_time():
    return int(5)

def generate_code():
    return random.SystemRandom().randrange(1000, 9999)
from .utils import send_template_email, get_expiration_time
from django.conf import settings
from accounts.models import CustomUser
import logging
logger = logging.getLogger(__name__)
        
def send_reset_request_mail(user, password):
    send_template_email(
        "utils/password_reset.html",
        user['email'],
        "Password Reset  MS Network",
        **{
            "name": user['username'],
            "password": password,
        },
    )
    
def send_signup_mail(data):
    send_template_email(
        "utils/signup.html",
        data['email'],
        "Your MS Network account have been created ",
        **{
            "app_name": 'MS Network',
            "data": data
        },
    )
    
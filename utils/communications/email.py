from .utils import send_template_email, get_expiration_time
from django.conf import settings
from accounts.models import CustomUser
import logging
logger = logging.getLogger(__name__)
        
def send_reset_request_mail(user_id, verification_code):
    user = CustomUser.objects.get(id=user_id)

    send_template_email(
        "utils/password_reset.html",
        user.email,
        "Password Reset",
        **{
            "name": user.first_name,
            "verification_link": 'https://myapi.nanocodes.com.ng/auth/confirm_password/',
            "otp_code": verification_code,
            "expiration_time": get_expiration_time(),
        },
    )
    
# def send_subscribe_mail(user, plan):
#     send_template_email(
#         "subscribe.html",
#         user.email,
#         "Subscription successful",
#         **{
#             "name": user.first_name,
#             "app_name": 'Andromeda',
#             "subscription_plan_name": plan
#         },
#     )
    
# def send_signup_mail(company_name, user_id):
#     user = CustomUser.objects.get(id=user_id)
#     send_template_email(
#         "signup.html",
#         user.email,
#         "Welcome Onboard",
#         **{
#             "name": user.first_name,
#             "company_name": company_name
#         },
#     )
    
# def send_add_team_mate_mail(user_id, company_id):
    # user = CustomUser.objects.get(id=user_id)
    # company = Company.objects.get(id=company_id)
    # send_template_email(
    #     "addteammate.html",
    #     user.email,
    #     "Welcome Onboard",
    #     **{
    #         "teammate_name": 'teammate_name',
    #         "company_name": company.name,
    #         "login_url":'login_url'
    #     },
    # )
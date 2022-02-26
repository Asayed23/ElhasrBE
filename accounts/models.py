from django.db import models

# Create your models here.

from rest_framework.response import Response
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    fullName = models.CharField(null=True,blank=False,max_length=100)


    phoneNumber= models.CharField(blank=True,max_length=50,default=None)
    # phoneNumber = models.IntegerField(blank=False,unique=True)
    
    
    email = models.CharField(null=True,max_length=100, verbose_name="Email")

    villaArea=models.IntegerField(null=True,blank=True,default=0)





class accountToken(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    token= models.CharField(blank=True,null=True,max_length=1000, verbose_name="token")
    def __str__(self):
        return self.token







from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

import smtplib 

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

#     # send_mail(
#     #     # title:
#     #     "Password Reset for {title}".format(title="Some website title"),
#     #     # message:
#     #     email_plaintext_message,
#     #     # from:
#     #     "pawpoint61@gmail.com.local",
#     #     # to:
#     #     [reset_password_token.user.email]
#     # )

# # creates SMTP session 
#     s = smtplib.SMTP('smtp.gmail.com', 587) 
  
#     # start TLS for security 
#     s.starttls() 
  
#         # Authentication 
#     s.login("pawpoint61@gmail.com", "pawpoint2021") 
  
#         # message to be sent 
#     subject = "password reset for sportive app"

#     message = "Subject: password reset for sportive app \n\n Password reset \n "+email_plaintext_message
  
#         # sending the mail 
#     # s.sendmail("pawpoint61@gmail.com", ["ahmedtawfik23@gmail.com"], message)
#     print(reset_password_token.user.email)
#     print("ahmed")
#     s.sendmail("pawpoint61@gmail.com", [reset_password_token.user.email], message) 
 
#         # terminating the session 
#     s.quit()
    # print("Hamada")
    context = {"data":email_plaintext_message}
    # return Response({"data":email_plaintext_message})

# class paymentProfile(models.Model):
#     user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
#     paymentType=models.CharField(null=True,max_length=100, verbose_name="paymentType")
    # paymentType=models.CharField(null=True,max_length=100, verbose_name="paymentType")
    # paidPeriod=

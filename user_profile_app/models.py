__author__ = "Marcin Roszczyk, .."
__license__ = "GPL"
__version__ = "0.0.1-pre-beta"
__maintainer__ = "Marcin Roszczyk"
__email__ = "mr@marcinros.net"
__status__ = "DEV"



from django.db import models
from django.contrib.auth.models import User


from datetime import datetime, time
from django.utils.translation import gettext_lazy as _



class ProjectSettings(models.Model):
    FRONTEND_URL = models.CharField(default='http://host.com:8000/', max_length=50, null=True, blank=True, help_text='Front-End URL')
    EMAIL_HOST= models.CharField(default='mailhost.roche.com', max_length=50, null=False, blank=False, help_text='Email server host')
    EMAIL_PORT=models.CharField(max_length=50, null=False, blank=False, default='587', help_text='e.g. 587 for SMTP') 
    EMAIL_HOST_USER=models.CharField(default='user@roche.com', max_length=50, null=False, blank=False, help_text='Usually email address of the sender')
    EMAIL_HOST_PASSWORD=models.CharField(default='12345!', max_length=20, null=True, blank=True, )
    SERVER_EMAIL=models.CharField(default='user@host.com', max_length=50, null=False, blank=False, help_text='Sender email')
    email_subject=models.CharField(default='Django Application', max_length=50, null=False, blank=False, help_text='Email subject')
    email_body=models.TextField(default='Django Application', null=False, blank=False, help_text='Email body')
    approver_email = models.EmailField(null=True, blank=True,  verbose_name='Approver Email', help_text='The person that approves accounta activation' )
    approver_required = models.BooleanField(verbose_name='Approver Required', default=True, help_text='If not set the account will be activated automatically')
    active = models.BooleanField(verbose_name='Active Settings', default=True, help_text='First settings from the active list will be used')
    
    def __str__(self):
      return str(self.EMAIL_HOST)

    class Meta:
      verbose_name = 'Settings'
      verbose_name_plural = 'Settings'



class UserProfile(models.Model):
    """ 
    Profile is associated to physical person and application user. One physical person may have multiple users and multiple User Profiles 
    <TBC>
    
    """
 
 
    USER_PROFILE_TYPE = (
    (1, 'Busines Analyst'),
    (2, 'Data Scientist'),
    (3, 'Admin'),
    )
     
 
    USER_PROFILE_DOCUMENT_ID_TYPE = (
        (1, 'National ID'),
        (2, 'Passport'),
        (3, 'Driving License'),
        (4, 'Other'),
    )

    first_login_date = models.DateTimeField(null=True, blank=True, verbose_name=_("first_login_date"))
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name=_("first_name"))
    last_name = models.CharField(max_length=30, null=False, blank=False, verbose_name=_("last_name"))
  
    personal_email = models.EmailField(blank=True, null=True, verbose_name=_("personal_email"))   
    #user_profile_image = models.ImageField(upload_to=user_directory_path , default="fob/images/user1.jpg", blank=True, null=True, verbose_name=_("user_profile_image")) 
    application_user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='application_user', verbose_name=_("application_user"))   
    user_profile_type = models.PositiveSmallIntegerField(choices=USER_PROFILE_TYPE , null=False, blank=False, default=1, verbose_name=_("USER_PROFILE_TYPE"))  
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    # def application_user_names(self):
    #     return [i for i in self.application_user.all()]

    def __str__(self):
        return str(self.personal_email)
        
    class Meta:
        verbose_name ="User Profile"
        verbose_name_plural = "User Profiles"


class SoftwareProduct(models.Model):
    """ 
    Software Product is associated to BU. A BU can have multiple Products 
    <TBC>
    
    """
 
    PRODUCT_TYPE = (
    (1, 'Software'),
    (2, 'SaaS'),
    (3, 'PaaS'),
    )
     
    product_name = models.CharField(max_length=30, null=False, blank=False, verbose_name=_("product_name"))


    def __str__(self):
        return str(self.product_name)
        
    class Meta:
        verbose_name ="Software Product"
        verbose_name_plural = "Software Products"

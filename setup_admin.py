from django.contrib.auth.models import User

if len(User.objects.filter(username='admin'))!=0:
    User.objects.create_superuser('admin','admin@gmail.com','Admin123!')
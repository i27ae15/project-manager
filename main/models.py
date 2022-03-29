from django.db import models
from django.contrib.auth.models import User
from djongo import models as dj_models


# everytime we modify the models we have to tell django
# python manage.py makemigrations appname
# python manage.py migrate

# t.item_set.all()

# <Item: Go to the mall>
# >>> t.item_set.all()
# <QuerySet [<Item: Go to the mall>]>
# >>> t.item_set.get(id=1)
# <Item: Go to the mall>
# >>> t.item_set.get(id=1).text
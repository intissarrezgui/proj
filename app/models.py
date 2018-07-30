from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


LOCATION_CHOICES = (
    ('Ariana'     , _('Ariana'     )),
    ('Beja'       , _('Beja'       )),
    ('Ben Arous'  , _('Ben Arous'  )),
    ('Bizerte'    , _('Bizerte'    )),
    ('Jendouba'   , _('Jendouba'   )),
    ('Gabes'      , _('Gabes'      )),
    ('Gafsa'      , _('Gafsa'      )),
    ('Kairouan'   , _('Kairouan'   )),
    ('Kasserine'  , _('Kasserine'  )),
    ('Kebili'     , _('Kebili'     )),
    ('Le Kef'     , _('Le Kef'     )),
    ('La Manouba' , _('La Manouba' )),
    ('Mahdia'     , _('Mahdia'     )),
    ('Medenine'   , _('Medenine'   )),
    ('Monastir'   , _('Monastir'   )),
    ('Nabeul'     , _('Nabeul'     )),
    ('Sfax'       , _('Sfax'       )),
    ('Sidi Bouzid', _('Sidi Bouzid')),
    ('Siliana'    , _('Siliana'    )),
    ('Sousse'     , _('Sousse'     )),
    ('Tunis'      , _('Tunis'      )),
    ('Tataouine'  , _('Tataouine'  )),
    ('Tozeur'     , _('Tozeur'     )),
    ('Zaghouan'   , _('Zaghouan'   )),
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=255)
    role = models.BooleanField()

    def __str__(self):
        return self.user.email

    def get_username(self):
        return self.user.username


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(choices=LOCATION_CHOICES, max_length=255)
    publish_date = models.DateTimeField(auto_now_add=True)
    budget = models.DecimalField(max_digits=10, decimal_places=3)
    employer = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Offer(models.Model):
    delivery_time = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    details = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='offers')
    freelancer = models.ForeignKey(Profile, on_delete=models.CASCADE)

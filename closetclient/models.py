from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
import datetime



# Create your models here.
class Profile(models.Model):
    """
    purpose: Creates Profile table within database
        Example useage:
    args: models.Model: (NA): models class given by Django
    returns: (None): N/A
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10)

    """Returns a string of account text to interact with interface """
    def __str__(self):  # __unicode__ on Python 2
        return self.user.account_name

    # listen for changes on user. update post-save
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # listen for changes on user. update post-save
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save() 

class Category(models.Model):
    """
    purpose: Creates Category table within database
        Example useage:
    args: models.Model: (NA): models class given by Django
    returns: (None): N/A
    """
    category_name = models.CharField(max_length=200, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.category_name

    def add_items(self):
        print(dir(self))
        return Item.objects.filter(item_category=self)


class Item(models.Model):
    """
    purpose: Creates Item table within database
        Example useage:
    args: models.Model: (NA): models class given by Django
    returns: (None): N/A
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # django will display a dropdown with these choices
    CATEGORY_CHOICES = (
        ('outerwear', 'OUTERWEAR'),
        ('tops', 'TOPS'),
        ('bottoms', 'BOTTOMS'),
        ('dresses', 'DRESSES'),
        ('shoes', 'SHOES'),
        ('bags', 'BAGS'),
        ('accessories', 'ACCESSORIES'),
        ('jewelry', 'JEWELRY'))

    item_category = models.ForeignKey(Category, on_delete=models.CASCADE, choices=CATEGORY_CHOICES)
    title = models.CharField(blank=False, max_length=255)
    description = models.TextField(null=False, max_length=500)
    brand = models.CharField(blank=True, max_length=255)
    image_path = models.ImageField(upload_to='images/', blank=True)

    class Meta:
        verbose_name_plural = 'items'

    """ returns a string of item text to interact with interface."""    
    def __str__(self):  # __unicode__ on Python 2
        return self.title        

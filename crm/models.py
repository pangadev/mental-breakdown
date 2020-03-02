from django.db import models
from datetime import datetime, timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
# import tagulous.models

# Create your models here.
class Contact(models.Model):
    SEX_CHOICES = (
        ('Female', 'Female',),
        ('Male', 'Male',),
        ('Unsure', 'Unsure',),
    )

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    birthdate = models.DateField()
    sex = models.CharField(choices=SEX_CHOICES, max_length=64, null=True, default="Unknown")
    description = models.CharField(max_length=600, blank="No description", null="True")
    contacts = models.ManyToManyField('self', through='ContactRelationship')
    activites = models.ForeignKey('Activity', related_name="contact_activity", on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(null=True)
    avatar = models.ImageField(upload_to='images/', null=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING,
                                   related_name='created_by')
    # slug = models.SlugField(unique=True, max_length=100)
    # tags = tagulous.models.TagField()


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        return int((datetime.now().date() - self.birthdate).days / 365.25)


class ContactRelationship(models.Model):
    types = models.ForeignKey('RelationshipType', blank=True,
                              related_name='contact_relationships', on_delete=models.CASCADE)
    from_contact = models.ForeignKey('Contact', related_name='from_contacts', on_delete=models.CASCADE)
    to_contact = models.ForeignKey('Contact', related_name='to_contacts', on_delete=models.CASCADE)


class RelationshipType(models.Model):
    name = models.CharField(max_length=64, null=True)
    from_type = models.CharField(max_length=64)
    to_type = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.to_type}"


class Activity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    activity_contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    #
    # def timeAfterUpdate(self):
    #     int(datetime.timedelta(days=datetime.now(timezone.utc)).total_seconds() // 3600)
    #     now = datetime.now(timezone.utc).total
    #     # now = datetime.now()
    #     timeAfter = self.updated_at - now
    #     # total =
    #     return (timeAfter)

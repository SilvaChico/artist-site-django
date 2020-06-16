from django.db import models
from django.urls import reverse
import uuid # Required for unique artwork instances
from django.contrib.postgres.fields.ranges import DateRangeField
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Gallery(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='images/logos/', height_field=None,
                             width_field=None, max_length=None, null=True, blank=True)
    address = models.CharField(max_length=90, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)


class Project(models.Model):
    name = models.CharField( max_length=50)
    

    def get_absolute_url(self):
        """Returns the url to access a particular project instance."""
        return reverse('project-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

class Artist(models.Model):
    """Model representing an artist."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    represented_by = models.ForeignKey(
        Gallery, help_text='Select a gallery that represents the artist, if any', on_delete=models.DO_NOTHING, null=True, blank=True)
    photograph = models.ImageField(
        upload_to='images/', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    portfolio = models.FileField(
        upload_to='documents/', max_length=100, null=True, blank=True)
    # Many To Many Field used because artwork can only have one artist, and artists can have multiple artworks
    artworks = models.ManyToManyField('ArtWork', null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    class Meta:
        ordering = ['first_name','last_name', ]

    def get_absolute_url(self):
        """Returns the url to access a particular artist instance."""
        return reverse('artist-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'

class MyProfile(Artist):
    class Meta:
        proxy = True
        verbose_name_plural = 'My Profile'
    
    def __str__(self):
        """String for representing the Model object."""
        return 'My Profile'

    def save(self, *args, **kwargs):
        if not self.pk and MyProfile.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised i n update of exists model
            raise ValidationError(
                'There is can be only one MyProfile instance')
        return super(MyProfile, self).save(*args, **kwargs)
    



class ArtWork(models.Model):
    """Model representing a artwork (but not a specific copy of a artwork)."""
    title = models.CharField(max_length=200)
    
    description = models.TextField(
        max_length=1000, help_text='Enter a description of the artwork', null=True, blank=True)
    medium_technique = models.CharField(
        'medium/technique', max_length=30, help_text='Enter the medium used in this art-piece', null=True, blank=True)
    
    # ForeignKey used because project can contain many artworks.But ab ArtWorks can only be in one project.
    # Genre class has already been defined so we can specify the object above.
    project = models.ForeignKey('Project', on_delete=models.DO_NOTHING,
                                help_text='Select a project for this artwork', null=True, blank=True)
    date = models.DateField((""), auto_now=False, auto_now_add=False, help_text='When was this artwork made')

    image = models.ImageField((""), upload_to='images/', height_field=None,
                              width_field=None, max_length=None, null=True, blank=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this artwork."""
        return reverse('artwork-detail', args=[str(self.id)])



class ArtWorkInstance(models.Model):
    """Model representing a specific copy of a artwork (i.e. that can be bought from the archive)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular artwork across whole archive')
    artwork = models.ForeignKey(
        'ArtWork', on_delete=models.SET_NULL, null=True)
    bought_by = models.CharField(max_length=200, null=True, blank=True)
    sold_date = models.DateField(null=True, blank=True)

    PIECE_STATUS = (
        ('n', 'Not for sale'),
        ('o', 'Being exhibited'),
        ('a', 'Available'),
        ('r', 'Reserved'),
        ('s', 'Sold'),
    )

    status = models.CharField(
        max_length=1,
        choices=PIECE_STATUS,
        blank=True,
        default='n',
        help_text='ArtWork availability',
    )

    class Meta:
        ordering = ['sold_date']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.artwork.title})'



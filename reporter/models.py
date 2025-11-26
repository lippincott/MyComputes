from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify

from django.utils.crypto import get_random_string
import hashlib

from django.utils import timezone

from PIL import Image, ExifTags

from django.db.models import Sum

# validators
from django.core.validators import FileExtensionValidator
from django.core import validators

from django import forms

#Unique IDs
import uuid
from django.utils.crypto import get_random_string

import datetime


###### IMAGES ########

## Validate Image size
def check_image_size(value):
    filesize = value.size
    if filesize:
        if filesize > 5000000:
            raise forms.ValidationError("Your image exceeds the maximum file size of 5 MB ")

def img_directory_path(instance, filename):
    today = datetime.datetime.now()
    today_path = today.strftime("%Y/%m%d%H%M%S")
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'img/{}/{}'.format(today_path, filename)


# Validate Image Dimensions
def check_image_dimensions(value):
    img_height = value.height
    img_width = value.width

    if img_height and img_width:

        if  img_width > 4032 or img_height > 4032:
            raise forms.ValidationError(f"Your image is {img_width}px x {img_height}px exceeds the maximum upload size of 4032px x 4032px")

        if  img_width < 400 or img_height < 400:
            raise forms.ValidationError(f"Your image is {img_width}px x {img_height}px less than the minimum upload size of 400px x 400px")


###### SLUGIFY ########
# Unique Slug Creator
def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=4)
    return unique_slug


TYPE_CHOICES = (
    ('', 'Beverage Type'),

    # -------------------------
    # High-Level Categories
    # -------------------------
    ('General', 'General'),
    ('Beer', 'Beer'),
    ('Wine', 'Wine'),
    ('Liquor', 'Liquor'),
    ('Liqueur', 'Liqueur'),
    ('Cider', 'Cider'),
    ('Mead', 'Mead'),
    ('Sake', 'Sake'),
    ('Hard Seltzer', 'Hard Seltzer'),
    ('Kombucha', 'Kombucha'),

    # -------------------------
    # Beer Styles
    # -------------------------
    ('Beer - Amber Ale', 'Beer - Amber Ale'),
    ('Beer - Barleywine', 'Beer - Barleywine'),
    ('Beer - Belgian Ale', 'Beer - Belgian Ale'),
    ('Beer - Belgian Witbier', 'Beer - Belgian Witbier'),
    ('Beer - Berliner Weisse', 'Beer - Berliner Weisse'),
    ('Beer - Bock', 'Beer - Bock'),
    ('Beer - Brown Ale', 'Beer - Brown Ale'),
    ('Beer - Doppelbock', 'Beer - Doppelbock'),
    ('Beer - Dunkel', 'Beer - Dunkel'),
    ('Beer - Farmhouse Ale', 'Beer - Farmhouse Ale'),
    ('Beer - Gose', 'Beer - Gose'),
    ('Beer - Hazy / New England IPA', 'Beer - Hazy / New England IPA'),
    ('Beer - Hefeweizen', 'Beer - Hefeweizen'),
    ('Beer - Helles', 'Beer - Helles'),
    ('Beer - Imperial Stout', 'Beer - Imperial Stout'),
    ('Beer - India Pale Ale (IPA)', 'Beer - India Pale Ale (IPA)'),
    ('Beer - Lager', 'Beer - Lager'),
    ('Beer - Lambic', 'Beer - Lambic'),
    ('Beer - Märzen / Oktoberfest', 'Beer - Märzen / Oktoberfest'),
    ('Beer - Milk Stout', 'Beer - Milk Stout'),
    ('Beer - Pale Ale', 'Beer - Pale Ale'),
    ('Beer - Pilsner', 'Beer - Pilsner'),
    ('Beer - Porter', 'Beer - Porter'),
    ('Beer - Saison', 'Beer - Saison'),
    ('Beer - Scotch Ale', 'Beer - Scotch Ale'),
    ('Beer - Sour Beer', 'Beer - Sour Beer'),
    ('Beer - Stout', 'Beer - Stout'),
    ('Beer - Triple IPA', 'Beer - Triple IPA'),
    ('Beer - Vienna Lager', 'Beer - Vienna Lager'),
    ('Beer - West Coast IPA', 'Beer - West Coast IPA'),
    ('Beer - Wheat Beer', 'Beer - Wheat Beer'),

    # -------------------------
    # Wine Types
    # -------------------------
    ('Wine - Albariño', 'Wine - Albariño'),
    ('Wine - Barbera', 'Wine - Barbera'),
    ('Wine - Cabernet Sauvignon', 'Wine - Cabernet Sauvignon'),
    ('Wine - Carménère', 'Wine - Carménère'),
    ('Wine - Cava', 'Wine - Cava'),
    ('Wine - Champagne', 'Wine - Champagne'),
    ('Wine - Chardonnay', 'Wine - Chardonnay'),
    ('Wine - Chenin Blanc', 'Wine - Chenin Blanc'),
    ('Wine - Dessert Wine', 'Wine - Dessert Wine'),
    ('Wine - Fortified Wine', 'Wine - Fortified Wine'),
    ('Wine - Grenache', 'Wine - Grenache'),
    ('Wine - Grüner Veltliner', 'Wine - Grüner Veltliner'),
    ('Wine - Ice Wine', 'Wine - Ice Wine'),
    ('Wine - Madeira', 'Wine - Madeira'),
    ('Wine - Malbec', 'Wine - Malbec'),
    ('Wine - Marsala', 'Wine - Marsala'),
    ('Wine - Merlot', 'Wine - Merlot'),
    ('Wine - Mourvèdre', 'Wine - Mourvèdre'),
    ('Wine - Moscato', 'Wine - Moscato'),
    ('Wine - Nebbiolo', 'Wine - Nebbiolo'),
    ('Wine - Petit Verdot', 'Wine - Petit Verdot'),
    ('Wine - Pinot Grigio / Pinot Gris', 'Wine - Pinot Grigio / Pinot Gris'),
    ('Wine - Pinot Noir', 'Wine - Pinot Noir'),
    ('Wine - Port', 'Wine - Port'),
    ('Wine - Prosecco', 'Wine - Prosecco'),
    ('Wine - Red Wine', 'Wine - Red Wine'),
    ('Wine - Riesling', 'Wine - Riesling'),
    ('Wine - Rosé', 'Wine - Rosé'),
    ('Wine - Sangiovese', 'Wine - Sangiovese'),
    ('Wine - Sauvignon Blanc', 'Wine - Sauvignon Blanc'),
    ('Wine - Sherry', 'Wine - Sherry'),
    ('Wine - Sparkling Wine', 'Wine - Sparkling Wine'),
    ('Wine - Sémillon', 'Wine - Sémillon'),
    ('Wine - Syrah / Shiraz', 'Wine - Syrah / Shiraz'),
    ('Wine - Tempranillo', 'Wine - Tempranillo'),
    ('Wine - Viognier', 'Wine - Viognier'),
    ('Wine - White Wine', 'Wine - White Wine'),
    ('Wine - Zinfandel', 'Wine - Zinfandel'),

    # -------------------------
    # Liquor / Spirits
    # -------------------------
    ('Liquor - Absinthe', 'Liquor - Absinthe'),
    ('Liquor - Aquavit', 'Liquor - Aquavit'),
    ('Liquor - Armagnac', 'Liquor - Armagnac'),
    ('Liquor - Blanco Tequila', 'Liquor - Blanco Tequila'),
    ('Liquor - Brandy', 'Liquor - Brandy'),
    ('Liquor - Bourbon', 'Liquor - Bourbon'),
    ('Liquor - Calvados', 'Liquor - Calvados'),
    ('Liquor - Canadian Whisky', 'Liquor - Canadian Whisky'),
    ('Liquor - Cognac', 'Liquor - Cognac'),
    ('Liquor - Dark Rum', 'Liquor - Dark Rum'),
    ('Liquor - Gin', 'Liquor - Gin'),
    ('Liquor - Grappa', 'Liquor - Grappa'),
    ('Liquor - Irish Whiskey', 'Liquor - Irish Whiskey'),
    ('Liquor - Japanese Whisky', 'Liquor - Japanese Whisky'),
    ('Liquor - London Dry Gin', 'Liquor - London Dry Gin'),
    ('Liquor - Mezcal', 'Liquor - Mezcal'),
    ('Liquor - Reposado Tequila', 'Liquor - Reposado Tequila'),
    ('Liquor - Rum', 'Liquor - Rum'),
    ('Liquor - Rye Whiskey', 'Liquor - Rye Whiskey'),
    ('Liquor - Scotch', 'Liquor - Scotch'),
    ('Liquor - Spiced Rum', 'Liquor - Spiced Rum'),
    ('Liquor - Tequila', 'Liquor - Tequila'),
    ('Liquor - Vodka', 'Liquor - Vodka'),
    ('Liquor - White Rum', 'Liquor - White Rum'),
    ('Liquor - Whiskey', 'Liquor - Whiskey'),

    # -------------------------
    # Liqueurs
    # -------------------------
    ('Liqueur - Amaro', 'Liqueur - Amaro'),
    ('Liqueur - Anise Liqueur', 'Liqueur - Anise Liqueur'),
    ('Liqueur - Coffee Liqueur', 'Liqueur - Coffee Liqueur'),
    ('Liqueur - Cream Liqueur', 'Liqueur - Cream Liqueur'),
    ('Liqueur - Fruit Liqueur', 'Liqueur - Fruit Liqueur'),
    ('Liqueur - Herbal Liqueur', 'Liqueur - Herbal Liqueur'),
    ('Liqueur - Orange Liqueur', 'Liqueur - Orange Liqueur'),
)




class Report(models.Model):
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(editable=False)
    last_modified = models.DateTimeField(null=True, blank=True)

    ## User Content
    brand = models.CharField(max_length=125, unique=False)
    product_name = models.CharField(max_length=125, unique=False)
    product_type = models.CharField(blank=False, max_length=125, default="General", choices=TYPE_CHOICES, unique=False)
    abv = models.FloatField(null=True, blank=True, unique=False)
    milliliters = models.FloatField(null=True, blank=True, unique=False)
    fl_oz = models.FloatField(null=True, blank=True, unique=False)
    warning_label = models.BooleanField(default=True)
    warning_text = models.CharField(max_length=512, null=True, blank=True, unique=False)

    ## AI Data
    ai_payload = models.TextField(unique=False, blank=True)
    ai_brand = models.CharField(max_length=125, blank=True, unique=False)
    ai_product_name = models.CharField(max_length=125, blank=True, unique=False)
    ai_product_type = models.CharField(unique=False, blank=True, max_length=125,)
    ai_abv = models.FloatField(null=True, blank=True, unique=False)
    ai_milliliters = models.FloatField(null=True, blank=True, unique=False)
    ai_fl_oz = models.FloatField(null=True, blank=True, unique=False)
    ai_warning_label = models.BooleanField(default=True)
    ai_warning_text = models.CharField(max_length=512, blank=True, unique=False)
    ai_error = models.CharField(max_length=255, blank=True, null=True)

    ## Match Scores
    match_brand = models.FloatField(null=True, blank=True)
    note_brand = models.CharField(max_length=300, blank=True, unique=False)

    match_product_name = models.FloatField(null=True, blank=True)
    note_product_name = models.CharField(max_length=300, blank=True, unique=False)

    match_product_type = models.FloatField(null=True, blank=True)
    note_product_type = models.CharField(max_length=300, blank=True, unique=False)

    match_abv = models.FloatField(null=True, blank=True)
    note_abv = models.CharField(max_length=300, blank=True, unique=False)

    match_milliliters = models.FloatField(null=True, blank=True)
    note_milliliters = models.CharField(max_length=300, blank=True, unique=False)

    match_fl_oz = models.FloatField(null=True, blank=True)
    note_fl_oz = models.CharField(max_length=300, blank=True, unique=False)

    match_warning_label = models.FloatField(null=True, blank=True)
    note_warning_label = models.CharField(max_length=300, blank=True, unique=False)

    match_warning_text = models.FloatField(null=True, blank=True)
    note_warning_text = models.CharField(max_length=300, blank=True, unique=False)



    ## Identifer
    slug = models.SlugField(max_length=150, allow_unicode=True, unique=True)

    ### front-image
    front_image = models.ImageField(upload_to=img_directory_path, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png',]), check_image_size],)

    ### back-image
    back_image = models.ImageField(upload_to=img_directory_path, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png',]), check_image_size ])


    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):

        if not self.created_at:
            self.created_at = timezone.now()
        else:
            self.last_modified = timezone.now()

        ## Slugs
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.product_name))

        super().save(*args, **kwargs)

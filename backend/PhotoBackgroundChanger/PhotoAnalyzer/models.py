from django.db import models

# Create your models here.


class Photo(models.Model):
    photo = models.ImageField(upload_to="photos/")
    created_at = models.DateTimeField(auto_now_add=True)


# Here we are not saving the photo in the database, we are only saving the id of the photo. The images will be stored automatically in the media folder.
# In the production we will use s3 bucket to store the images.

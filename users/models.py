from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='default_avatar.jpg', upload_to='profile_images')

    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar and hasattr(self.avatar, 'path'):
            try:
                img = Image.open(self.avatar.path)
                if img.height > 250 or img.width > 250:
                    new_img = (250, 250)
                    img.thumbnail(new_img)
                    img.save(self.avatar.path)
            except (FileNotFoundError, ValueError):
                pass
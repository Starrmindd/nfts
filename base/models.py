from django.db import models
from django.contrib.auth.models import User



class NFT(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)  # Optional, can be NULL in the database
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True,)
    image = models.ImageField(upload_to='nft_images/', null=True, blank=True)  # Optional, can be NULL
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Owner can be NULL
    token_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Token ID can be NULL

    def __str__(self):
        return self.name
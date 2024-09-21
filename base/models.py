# marketplace/models.py

from django.db import models
from django.contrib.auth.models import User

class NFT(models.Model):
    token_id = models.CharField(max_length=100, unique=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image_url = models.URLField(null=True)
    description = models.TextField(null=True)
    is_for_sale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"NFT {self.token_id}"
    
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255, null=True, blank=True)
    private_key = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Transaction(models.Model):
    buyer = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='sales', on_delete=models.CASCADE)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.nft.token_id}"
    


from django.db import models
from django.utils import timezone
from django.conf import settings



from django.db import models
from django.utils import timezone

class Auction(models.Model):
    # NFT Details included directly in the model
    nft_image = models.FileField(upload_to='nft_images/', blank=True, null=True)
    nft_title = models.CharField(max_length=255, help_text="Title of the NFT",null=True)
    description = models.TextField(help_text="Detailed description of the NFT",null=True)
    creator_name = models.CharField(max_length=255,null=True, help_text="Name of the original creator/artist")
    nft_collection = models.CharField(max_length=255, null=True, blank=True, help_text="Collection the NFT belongs to")
    token_id = models.CharField(max_length=100, unique=True, help_text="Unique identifier of the NFT",null=True)
    seller_wallet =models.CharField(max_length=255, help_text="Wallet Address",null=True)

    # Auction Details
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='winning_bid')
    is_active = models.BooleanField(default=True)


    is_sold = models.BooleanField(default=False)  # Indicates if the NFT is sold
    is_listed = models.BooleanField(default=False)
    admin_list =models.BooleanField(default=False)  # Indica
    def __str__(self):
        return f"Auction for {self.nft_title}"

class Ownership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Buyer of the NFT
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)  # Auction/NFT associated with the buyer
    purchase_date = models.DateTimeField(auto_now_add=True)  # Date of purchase

    def __str__(self):
        return f"{self.user.username} owns {self.auction.nft_title}"

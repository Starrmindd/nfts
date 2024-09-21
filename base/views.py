from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import NFT, Transaction, UserProfile
from django.contrib.auth import login
from django.utils.crypto import get_random_string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import NFT, Transaction, UserProfile
from .web import transfer_nft  # Ensure this function is properly defined
from django.conf import settings

from django.contrib.auth import login, get_user_model
from django.utils.crypto import get_random_string
from .models import UserProfile


# def buy_nft(request, token_id):
#     user = get_or_create_anonymous_user(request)
#     nft = get_object_or_404(NFT, token_id=token_id)
#     if request.method == 'POST':
#         if nft.is_for_sale and nft.price:
#             buyer = user
#             seller_profile = get_object_or_404(UserProfile, user=nft.owner)
#             buyer_profile = get_or_create_anonymous_user(request)  # No need to query again

#             # Create transaction record
#             transaction = Transaction.objects.create(
#                 buyer=buyer,
#                 seller=nft.owner,
#                 nft=nft,
#                 price=nft.price
#             )

#             # Perform Web3 transaction (mocking here)
#             try:
#                 tx_hash = transfer_nft(
#                     from_address=seller_profile.wallet_address,
#                     to_address=buyer_profile.wallet_address,
#                     token_id=nft.token_id,
#                     private_key=seller_profile.private_key
#                 )
#                 print(f"Transaction hash: {tx_hash.hex()}")

#                 # Update NFT ownership
#                 nft.owner = buyer
#                 nft.is_for_sale = False
#                 nft.save()

#                 return redirect('nft_list')

#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 return render(request, 'nf.html', {'nft': nft, 'error': 'An error occurred during the transaction.'})

#     return render(request, 'nf.html', {'nft': nft})



from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Auction, NFT
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
import pytz
from .models import Auction, NFT
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
import pytz
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Auction

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Auction
import pytz
from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import datetime
import pytz

# Custom test to check if the user is a superuser (admin)
def is_admin(user):
    return user.is_superuser

# Only allow logged-in users who are admins to access the view
@login_required(login_url='login')  # First check if the user is logged in
@user_passes_test(is_admin, login_url='/login/')  # Then check if the user is an admin
def create_auction(request):
    if request.method == 'POST':
        # Extract form data manually
        nft_image = request.FILES.get('nft_image')  # Handle file upload
        nft_title = request.POST.get('nft_title')
        description = request.POST.get('description')
        creator_name = request.POST.get('creator_name')
        nft_collection = request.POST.get('nft_collection')
        token_id = request.POST.get('token_id')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        starting_price = request.POST.get('starting_price')
        seller_wallet = request.POST.get('seller_wallet')
        current_price = request.POST.get('current_price', 0)  # Default to 0 if not provided
        is_active = request.POST.get('is_active') == 'true'  # Checkbox or radio button for active status

        try:
            # Convert string date/time to naive datetime objects
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            return HttpResponse("Invalid date/time format", status=400)

        # Convert naive datetime to timezone-aware datetime
        tz = pytz.timezone('UTC')  # Adjust to your timezone if necessary
        start_time = tz.localize(start_time)
        end_time = tz.localize(end_time)

        # Check if an auction already exists for this token ID
        if Auction.objects.filter(token_id=token_id).exists():
            return HttpResponse("Auction already exists for this NFT", status=400)

        # Create and save the auction manually
        auction = Auction(
            nft_image=nft_image,  # Assign the file uploaded by the user
            nft_title=nft_title,
            description=description,
            creator_name=creator_name,
            nft_collection=nft_collection,
            token_id=token_id,
            start_time=start_time,
            end_time=end_time,
            starting_price=starting_price,
            current_price=current_price,
            is_active=is_active,
            seller_wallet=seller_wallet,
            owner=request.user,  # Set the owner to the currently logged-in user (admin)
            admin_list=True
        )
        auction.save()  # Save the auction object to the database
        return redirect('adminview')

    return render(request, 'create_auction.html')


@login_required(login_url="login")
def auction_list(request):
    # Close expired auctions before listing
    Auction.objects.filter(end_time__lt=timezone.now(), is_active=True).update(is_active=False)

    # Filter active auctions that are not sold and not listed
    auctions = Auction.objects.filter(is_active=True,is_listed=False,is_sold=False,admin_list=True)
    seller = Auction.objects.filter(is_active=True,is_listed=True,is_sold=True)
    return render(request, 'auction_list.html', {'auctions': auctions,'seller':seller})

@login_required(login_url="login")
def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    # Ensure auction is closed if necessary
    if auction.end_time < timezone.now():
        auction.is_active = False
        auction.save()

    if request.method == 'POST':
        bid_amount = float(request.POST.get('bid_amount'))
        if bid_amount > auction.current_price:
            auction.current_price = bid_amount
            auction.highest_bidder = request.user
            auction.save()
            return redirect('auction_detail', auction_id=auction.id)

    return render(request, 'auction_detail.html', {'auction': auction})




from django.contrib.auth import login, authenticate
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("Passwords do not match.")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username is already taken.")

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email is already registered.")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        
        return redirect('login')

    return render(request, 'register.html')
from django.contrib import auth

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('auction_list')  # Change 'home' to your desired redirect URL
        else:
            return HttpResponse("Invalid username or password.")
 
    return render(request, 'login.html')

def index(request):
    return render (request, 'index.html')


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NFT, Transaction
from  base.utils import process_payment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import NFT, Transaction ,Ownership
from web3 import Web3
from web3.exceptions import InvalidAddress, TransactionNotFound, ContractLogicError

# Set up Web3 with your Infura endpoint
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/a334486f863d447c90f3e07f12f6c582"))
@login_required(login_url="login")
def buy_nft(request, nft_title):
    # Retrieve the NFT based on its title
    nft = get_object_or_404(Auction, nft_title=nft_title)

    if request.method == 'POST':
        wallet_address = request.POST.get('wallet_address')
        private_key = request.POST.get('private_key')

        # Validate the wallet address and private key
        if not wallet_address or not private_key:
            messages.error(request, "Wallet address and private key are required.")
            return redirect('buy_nft', nft_title=nft_title)

        # Ensure the NFT has a seller assigned
        buyer = request.user
        seller = nft.owner

        # Check if the NFT is still available for sale
        if not nft.is_active:
            messages.error(request, "This NFT is no longer available for sale.")
            return redirect('buy_nft', nft_title=nft_title)

        # Payment Logic: Process the transaction using Web3
        seller_wallet = nft.seller_wallet
        nft_price = nft.current_price

        # try:
            # Convert ETH to Wei
            # nft_price_in_wei = web3.to_wei(nft_price, 'ether')

            # # Get the nonce for the buyer's wallet address
            # nonce = web3.eth.get_transaction_count(wallet_address)

            # # Create the transaction details
            # transaction = {
            #     'nonce': nonce,
            #     'to': seller_wallet,
            #     'value': nft_price_in_wei,
            #     'gas': 21000,  # You can adjust this as needed
            #     'gasPrice': web3.to_wei('50', 'gwei'),
            # }

            # # Sign the transaction with the buyer's private key
            # signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

            # # Send the transaction to the blockchain
            # tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

            # # Wait for the transaction to be confirmed
            # web3.eth.wait_for_transaction_receipt(tx_hash)
            
        nft.seller_wallet = wallet_address  # Update seller wallet to buyer's wallet
        nft.owner = buyer  # Change ownership to the buyer
        nft.is_active = False 
        nft.is_listed = True  # Remove from general market
        nft.save() # Mark as sold
     

        # **Create the Ownership Record for the Buyer:**
        Ownership.objects.create(
            user=buyer,
            auction=nft  # Link the auction/NFT to the buyer
        )
        # Record the transaction in the database
        # Transaction.objects.create(
        #     buyer=request.user,
        #     seller=seller,
        #     nft=nft,
        #     price=nft.current_price
        # )
# ?{tx_hash.hex()}
        # Mark the NFT as sold
        nft.is_active = False
        nft.save()

        # Success message
        messages.success(request, f"Purchase successful! Transaction Hash: ")
        return redirect('purchase')

        # except InvalidAddress:
        #     messages.error(request, "Transaction failed: Invalid wallet address provided.")
        # except ValueError as ve:
        #     error_message = str(ve)
        #     if 'insufficient funds' in error_message.lower():
        #         messages.error(request, "Transaction failed: Insufficient funds in the wallet.")
        #     else:
        #         messages.error(request, f"Transaction failed: {error_message}")
        # except TransactionNotFound:
        #     messages.error(request, "Transaction not found. Please try again.")
        # except ContractLogicError:
        #     messages.error(request, "Transaction failed due to smart contract logic.")
        # except Exception as e:
        #     messages.error(request, f"An unexpected error occurred: {str(e)}")

        # # Redirect back to the buy page on error
        # return redirect('buy_nft', nft_title=nft_title)

    return render(request, 'buy_nft.html', {'nft': nft})
 

from django.shortcuts import render
from .models import Ownership, Auction

def buyer_nft_list(request):
    # Get all NFTs the current user owns
    owned_nfts = Ownership.objects.filter(user=request.user)

    return render(request, 'buyer_nft_list.html', {
        'owned_nfts': owned_nfts
    })


from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .models import Auction

def list_nft_for_sale(request):
    if request.method == 'POST':
        nft_id = request.POST.get('nft_id')
        price = request.POST.get('price')

        try:
            # Get the NFT the buyer owns
            nft = Auction.objects.get(id=nft_id, owner=request.user)

            if nft.is_sold:
                messages.error(request, "This NFT is already sold and cannot be listed again.")
                return redirect('purchase')

            # Update the NFT details to list it for sale
            nft.is_active = True  # Mark it as available for sale again
            nft.is_listed = True  # Mark as listed for sale
            nft.is_sold = True  # Mark as not sold
            nft.current_price = price  # Set the new price
            nft.start_time = timezone.now()  # Update start time
            nft.end_time = timezone.now() + timezone.timedelta(days=100)  # Set an auction end time (e.g., 7 days from now)
             # Automatically update seller wallet to buyer's wallet address

            nft.save()

            messages.success(request, "Your NFT has been listed for sale!")
        except Auction.DoesNotExist:
            messages.error(request, "NFT not found or you're not the owner of this NFT.") 
        except ValueError:
            messages.error(request, "Please enter a valid price.")

        return redirect('purchase')
    

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Auction
def delist_nft(request, nft_id):
    # Fetch the NFT to delist, ensuring the owner is the current user
    nft = Auction.objects.get(id=nft_id, owner=request.user)

    if not nft.is_listed:
        messages.error(request, "This NFT is not currently listed for sale.")
        return redirect('purchase')

    # Update the auction details to delist the NFT
    nft.is_sold = False  # Reset sold status if needed
    nft.is_listed = False  # Mark it as delisted
    nft.is_active = False  # Mark it as not active
    nft.save()

    messages.success(request, "Your NFT has been delisted.")
    return redirect('purchase')
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

# Custom check function to verify if user is an admin
def is_admin(user):
    return user.is_superuser  # Returns True if the user is an admin

@user_passes_test(is_admin, login_url='/login/')
def adminview(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated
    admin = Auction.objects.filter(is_active=True)
    context = {
        'admin': admin
    }
    return render(request, 'adminview.html', context)



def delist_admin(request, pk):
    admin = get_object_or_404(Auction, pk=pk)  # Fetch Auction with given pk
    admin.admin_list = False  # Set to delisted
    admin.save()
    return redirect('adminview')  # Redirect to admin view page

def list_admin(request, pk):
    admin = get_object_or_404(Auction, pk=pk)  # Fetch Auction with given pk
    admin.admin_list = True  # Set to listed
    admin.save()
    return redirect('adminview')  # Redirect to admin view page

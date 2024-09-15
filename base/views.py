from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from web3 import Web3


from django import forms
from .models import NFT
class NFTListingForm(forms.ModelForm):
    class Meta:
        model = NFT
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            # If you have a date field, use this widget
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


@login_required(login_url='login') 
def listnft(request):
    if request.method == 'POST':
        form = NFTListingForm(request.POST, request.FILES)
        if form.is_valid():
            nft = form.save(commit=False)
            nft.owner = request.user
            # Generate a unique token_id here, for example:
            nft.token_id = generate_unique_token_id()
            nft.save()
            return redirect('nft_detail', nft_id=nft.id)  # Redirect to a detail page or another relevant page
    else:
        form = NFTListingForm()

    return render(request, 'list-nft.html', {'form': form})

def generate_unique_token_id():
    # Logic to generate a unique token ID
    import uuid
    return str(uuid.uuid4())

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


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
            return redirect('/')  # Change 'home' to your desired redirect URL
        else:
            return HttpResponse("Invalid username or password.")
 
    return render(request, 'login.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  

from django.shortcuts import render, get_object_or_404
from .models import NFT

@login_required(login_url='login') 
def nft_detail(request, nft_id):
    nft = get_object_or_404(NFT, id=nft_id)
    return render(request, 'nft-details.html', {'nft': nft})

from django.shortcuts import render
from .models import NFT

def nft_list(request):
    """Render the NFT listing page with all NFTs, optionally filtered by search query."""
    search_query = request.GET.get('search', '')
    nfts = NFT.objects.all()
    
    if search_query:
        nfts = nfts.filter(name__icontains=search_query)  # Filter NFTs by name

    return render(request, 'nft.html', {'nfts': nfts})

from django.shortcuts import render
from .models import NFT

def index(request):
    """Render the home page with featured NFTs."""
    featured_nfts = NFT.objects.all()[:6]  # Adjust the query as needed to get featured NFTs
    return render(request, 'index.html', {'featured_nfts': featured_nfts})

 
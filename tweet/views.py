from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def index(request):
    return render(request, 'index.html')
    

def tweet_list(request):
    tweets = Tweet.objects.all()
    return render(request, 'tweet_list.html', {'tweets': tweets})


@login_required(login_url='login')
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})


@login_required(login_url='login')
def update_tweet(request, tweet_id):
    tweet= get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)  
    return render(request, 'tweet_form.html', {'form': form})

@login_required(login_url='login')
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect('tweet_list')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Wellcome back, {username}!')
            return redirect('tweet_list')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, f'You have logged out.')
    return redirect('tweet_list')                               


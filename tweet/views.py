from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from .forms import TweetForm

def index(request):
    return render(request, 'index.html')
    

def tweet_list(request):
    tweets = Tweet.objects.all()
    return render(request, 'tweet_list.html', {'tweets': tweets})



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



def update_tweet(request, pk):
    tweet= get_object_or_404(Tweet, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)  
    return render(request, 'tweet_form.html', {'form': form})


def delete_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk, user=request.user)

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

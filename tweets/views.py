from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, View

from tweets.forms import CreateTweetForm

# from django.db.models import Count  # modelsをインポート
from .models import Like, Tweet


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "tweets/home.html"
    context_object_name = "tweets"

    def get_queryset(self):
        return Tweet.objects.all().select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_likes = Like.objects.filter(likeuser=self.request.user).values_list("liketweet_id", flat=True)
        for tweet in context["tweets"]:
            tweet.liked_by_user = tweet.id in user_likes
        return context


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/create.html"
    model = Tweet
    form_class = CreateTweetForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweets/detail.html"
    model = Tweet

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tweet = self.object

        user_likes = set(Like.objects.filter(likeuser=self.request.user).values_list("liketweet_id", flat=True))
        tweet.liked_by_user = tweet.id in user_likes

        context["user"] = self.request.user
        context["tweet"] = tweet
        return context


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "tweets/delete.html"
    model = Tweet
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)


class LikeView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        likedtweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        if not Like.objects.filter(likeuser=self.request.user, liketweet=likedtweet).exists():
            Like.objects.create(likeuser=self.request.user, liketweet=likedtweet)
            likedtweet.like_count += 1
            likedtweet.save()
            liked = True
        else:
            liked = False
        return JsonResponse({"status": "ok", "is_liked": liked, "total_likes": likedtweet.like_count})


class UnlikeView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        unlikedtweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        like_instance = Like.objects.filter(likeuser=self.request.user, liketweet=unlikedtweet).first()
        if like_instance:
            like_instance.delete()
            unlikedtweet.like_count -= 1
            unlikedtweet.save()
            liked = False
        else:
            liked = True
        return JsonResponse({"status": "ok", "is_liked": liked, "total_likes": unlikedtweet.like_count})

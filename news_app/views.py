from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.expressions import result
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from .models import Category, Comment
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ContactForm, CommentForm
from .models import News
from config.custom_permissions import OnlyLoggedSuperUser
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

class NewsTitleView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'news/news_list.html'


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, status='PB')
    comments = news.comments.filter(active=True)
    new_comment = None
    # HitCount uchun object olish
    hit_count = HitCount.objects.get_for_object(news)
    # HitCount-ni oshirish (har bir yangilik uchun alohida)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi komment obyektni yaratamiz lekin DB ga saqlamaymiz commit=False orqali
            new_comment = comment_form.save(commit=False)
            # comment qaysi yangilikka tegishliligini turgan yangiligiga tengladik
            new_comment.news = news
            # Izoh egasini so'rov yuboroyatganga uladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'news': news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }

    return render(request, 'news/news_detail.html', context=context)



class DetailPageView(HitCountDetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    count_hit = True


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(news= self.get_object()).order_by('-created_time')
        data['comments'] = comments_connected
        data['comments_count'] = len(comments_connected)
        if self.request.user.is_authenticated:
            data['comments_form'] = CommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        news_object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.news = news_object
            comment.save()
        return self.get(request, *args, **kwargs)

class HomeView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(
            status='PB'
        ).order_by('-publish_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # top news (first 4)
        context['top_news'] = self.get_queryset()[:4]

        # main news list (first 10)
        context['news_list'] = self.get_queryset()[:10]

        categories = Category.objects.all()

        for category in categories:
            context[category.name.lower()] = News.objects.filter(
                category=category
            ).order_by('-publish_time')

        return context


class ContactView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<h2>biz bilan boglanganinggiz uchun raxmaat <h2/>")
        context = {'form': form}

        return render(request, 'news/contact.html', context=context)

class BusinessNewsView(ListView):
    model = News
    template_name = 'news/business.html'
    context_object_name = 'business_news'

    def get_queryset(self):
        news = News.objects.filter(category__name='Biznes').order_by('-publish_time')
        return news


class SocialNewsView(ListView):
    model = News
    template_name = 'news/social.html'
    context_object_name = 'social_news'

    def get_queryset(self):
        news = News.objects.filter(category__name='Jamiyat').order_by('-publish_time')
        return news

class PoliticsNewsView(ListView):
    model = News
    template_name = 'news/politics.html'
    context_object_name = 'politics_news'

    def get_queryset(self):
        news = News.objects.filter(category__name='Siyosat').order_by('-publish_time')
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = News.objects.filter(category__name='Sport').order_by('-publish_time')
        return news

class UpdateNewsView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'

class DeleteNewsView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home')

class NewsCreateView(OnlyLoggedSuperUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminpage(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultsView(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return News.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query)
            )
        return News.objects.none()




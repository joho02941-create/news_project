

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Category

from .forms import ContactForm
from .models import News

class NewsTitleView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'news/news_list.html'

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'



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


from django.urls import path
from .views import NewsTitleView, NewsDetailView, HomeView, ContactView, BusinessNewsView, SocialNewsView, PoliticsNewsView, SportNewsView

urlpatterns = [
    path('news/',  NewsTitleView.as_view() , name= 'all_news_list'),
    path('news/<slug:slug>/',NewsDetailView.as_view() , name= 'news_detail_page'),
    path('', HomeView.as_view() , name= 'home'),
    path('contact/', ContactView.as_view() , name= 'contact_page'),
    path('business/', BusinessNewsView.as_view() , name= 'business_news_list'),
    path('social/', SocialNewsView.as_view() , name= 'social_news_list'),
    path('politis/', PoliticsNewsView.as_view() , name= 'politis_news_list'),
    path('sport/', SportNewsView.as_view() , name= 'sport_news_list'),
]


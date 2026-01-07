from django.urls import path
from .views import NewsTitleView, DetailPageView, HomeView, ContactView, BusinessNewsView, news_detail, \
    SocialNewsView, PoliticsNewsView, SportNewsView, UpdateNewsView, DeleteNewsView, NewsCreateView, adminpage, SearchResultsView

urlpatterns = [
    path('news/',  NewsTitleView.as_view() , name= 'all_news_list'),
    path('news/<slug:slug>/',DetailPageView.as_view(), name= 'news_detail_page'),
    path('news/create', NewsCreateView.as_view() , name= 'news_create'),
    path('news/<slug:slug>/edit', UpdateNewsView.as_view() , name= 'edit_news'),
    path('news/<slug:slug>/delete', DeleteNewsView.as_view(), name= 'delete_news'),
    path('', HomeView.as_view() , name= 'home'),
    path('contact/', ContactView.as_view() , name= 'contact_page'),
    path('business/', BusinessNewsView.as_view() , name= 'business_news_list'),
    path('social/', SocialNewsView.as_view() , name= 'social_news_list'),
    path('politis/', PoliticsNewsView.as_view() , name= 'politis_news_list'),
    path('sport/', SportNewsView.as_view() , name= 'sport_news_list'),
    path('adminpage/', adminpage , name= 'admin_page'),
    path('search/', SearchResultsView.as_view() , name= 'search_results'),
]



from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('get_data/', views.get_data, name='get_data'),
    path('trades/', views.trades, name='trades'),
    path('bars/', views.bars, name='bars'),
    path('downloadbars/', views.bars, name='downloadbars'),
    path('downloadbarssubmit/', views.submitb, name="downloadbarssubmit"),
    path('downloadtrades/', views.trades, name='downloadtrades'),
    path('downloadtradessubmit/', views.submitt, name="downloadtradessubmit"),
    path('about/', views.about, name="about"),
    path('projects/', views.projects, name="projects"),
    path('contact/', views.contact, name="contact"),
    path('cpquant/', views.contact, name="cpquant"),
    path('startup-valuation/', views.startup_valuation, name="startup- valuation"),
    path('mts/', views.mts, name="mts"),
]

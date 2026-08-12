from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict', views.predict, name='predict'),
    path('metrics', views.get_metrics_endpoint, name='metrics'),
    path('train', views.train_model, name='train'),
    path('train/stream', views.train_stream, name='train_stream'),
    path('feature_importance', views.get_feature_importance, name='feature_importance'),
    path('notebook', views.get_notebook_html, name='notebook'),
]

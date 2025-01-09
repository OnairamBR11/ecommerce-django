from django.urls import path
from .views import ProdutoListCreateView

urlpatterns = [
    path('produto/', 
         ProdutoListCreateView.as_view(), 
         name='produto-list-create'),
]


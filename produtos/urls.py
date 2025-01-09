from django.urls import path
from .views import ProdutoListCreateView, ProdutoDetailView

urlpatterns = [
    path('produtos/', ProdutoListCreateView.as_view(), name='produto-list-create'),
    path('produtos/<int:pk>/', ProdutoDetailView.as_view(), name='produto-detail'),  # Nome da URL corrigido
]


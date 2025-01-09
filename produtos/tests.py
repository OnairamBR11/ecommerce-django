from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Produto

class ProdutoTests(APITestCase):
    def setUp(self):
        # Cria um usuário para autenticação
        self.user = User.objects.create_user(username='usuarioTeste', password='teste12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Autentica o usuário

        # Cria um produto para testes
        self.produto = Produto.objects.create(nome='Notebook', preco=500.0, estoque=10, descricao='Notebook Samsung')

    def test_listar_produtos(self):
        """
        Testa se a listagem de produtos funciona.
        """
        url = reverse('produto-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Verifica se retornou 1 produto

    def test_criar_produto(self):
        """
        Testa a criação de um novo produto.
        """
        url = reverse('produto-list-create')
        data = {'nome': 'Smartphone', 'preco': 1500.00, 'descricao': 'Telefone samsung', 'estoque': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 2)  # Verifica se o produto foi criado

    def test_detalhes_produto(self):
        """
        Testa se os detalhes de um produto são retornados corretamente.
        """
        url = reverse('produto-detail', args=[self.produto.id])  # Corrigido: 'produto-detail'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Notebook')  # Verifica o nome do produto

    def test_atualizar_produto(self):
        """
        Testa a atualização de um produto.
        """
        url = reverse('produto-detail', args=[self.produto.id])
        data = {'nome': 'Notebook Atualizado', 'descricao': 'Notebook samsung', 'preco': 5500.00, 'estoque': 8}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Notebook Atualizado')  # Verifica se o nome foi atualizado

    def test_deletar_produto(self):
        """
        Testa a exclusão de um produto.
        """
        url = reverse('produto-detail', args=[self.produto.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Produto.objects.count(), 0)  # Verifica se o produto foi deletado

    def test_obter_token(self):
        """
        Testa se o endpoint de login retorna um token válido.
        """
        url = reverse('token_obtain_pair')
        data = {'username': 'usuarioTeste', 'password': 'teste12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Verifica se o token de acesso foi retornado
        self.assertIn('refresh', response.data)  # Verifica se o token de refresh foi retornado

    def test_acesso_protegido_sem_token(self):
        """
        Testa se um endpoint protegido retorna erro 401 sem token.
        """
        self.client.force_authenticate(user=None)  # Remove a autenticação
        url = reverse('produto-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acesso_protegido_com_token(self):
        """
        Testa se um endpoint protegido pode ser acessado com token válido.
        """
        # Obtém o token de acesso
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Configura o header de autenticação
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Tenta acessar o endpoint protegido
        url = reverse('produto-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Publicacao


class PublicacaoModelTest(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user(username='autor', password='123')
        self.publicacao = Publicacao.objects.create(
            titulo='Teste',
            slug='teste',
            conteudo='Conteúdo de teste',
            autor=self.autor,
        )

    def test_str_retorna_titulo(self):
        self.assertEqual(str(self.publicacao), 'Teste')

    def test_ordenacao_decrescente_por_data(self):
        Publicacao.objects.create(titulo='Segunda', slug='segunda', conteudo='...', autor=self.autor)
        publicacoes = Publicacao.objects.all()
        self.assertGreater(publicacoes[0].data_criacao, publicacoes[1].data_criacao)


class PaginaInicialViewTest(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user(username='autor', password='123')
        for i in range(5):
            Publicacao.objects.create(
                titulo=f'Post {i}',
                slug=f'post-{i}',
                conteudo='Conteúdo',
                autor=self.autor,
            )

    def test_status_code_200(self):
        response = self.client.get(reverse('pagina_inicial'))
        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        response = self.client.get(reverse('pagina_inicial'))
        self.assertTemplateUsed(response, 'blog/pagina_inicial.html')

    def test_context_tem_publicacoes(self):
        response = self.client.get(reverse('pagina_inicial'))
        self.assertIn('publicacoes', response.context)


class DetalhePublicacaoViewTest(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user(username='autor', password='123')
        self.publicacao = Publicacao.objects.create(
            titulo='Teste Detalhe',
            slug='teste-detalhe',
            conteudo='Conteúdo do detalhe',
            autor=self.autor,
        )

    def test_status_code_200(self):
        response = self.client.get(reverse('detalhe_publicacao', args=['teste-detalhe']))
        self.assertEqual(response.status_code, 200)

    def test_404_para_slug_invalido(self):
        response = self.client.get(reverse('detalhe_publicacao', args=['slug-inexistente']))
        self.assertEqual(response.status_code, 404)

    def test_incrementa_visualizacoes(self):
        self.client.get(reverse('detalhe_publicacao', args=['teste-detalhe']))
        self.publicacao.refresh_from_db()
        self.assertEqual(self.publicacao.visualizacoes, 1)

from django.db import IntegrityError
from django.test import TestCase

from ..models import Categoria, Publicacao
from .test_base import BaseTeste


class CategoriaModeloTeste(TestCase):
    def test_str_retorna_nome(self):
        cat = Categoria.objects.create(nome="Tecnologia", slug="tecnologia")
        self.assertEqual(str(cat), "Tecnologia")

    def test_slug_unico(self):
        Categoria.objects.create(nome="Tech", slug="tech")
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nome="Tech 2", slug="tech")

    def test_ordenacao_por_nome(self):
        c1 = Categoria.objects.create(nome="Zebra", slug="zebra")
        c2 = Categoria.objects.create(nome="Alpha", slug="alpha")
        cats = list(Categoria.objects.all())
        self.assertEqual(cats, [c2, c1])

    def test_descricao_opcional(self):
        cat = Categoria.objects.create(nome="X", slug="x")
        self.assertEqual(cat.descricao, "")


class PublicacaoModeloTeste(BaseTeste):
    def test_string_retorna_titulo(self):
        self.assertEqual(str(self.publicacao), "Teste")

    def test_ordenacao_decrescente_por_data(self):
        Publicacao.objects.create(
            titulo="Segunda", slug="segunda", conteudo="...", autor=self.autor
        )
        publicacoes = Publicacao.objects.all()
        self.assertGreater(publicacoes[0].data_criacao, publicacoes[1].data_criacao)

    def test_slug_unico(self):
        with self.assertRaises(IntegrityError):
            Publicacao.objects.create(
                titulo="Outro", slug="teste", conteudo="...", autor=self.autor
            )

    def test_subtitulo_pode_ser_vazio(self):
        p = Publicacao.objects.create(
            titulo="Sem subtitulo", slug="sem-subtitulo", autor=self.autor
        )
        self.assertEqual(p.subtitulo, "")

    def test_visualizacoes_padrao_zero(self):
        p = Publicacao.objects.create(
            titulo="Novo", slug="novo", autor=self.autor
        )
        self.assertEqual(p.visualizacoes, 0)

    def test_autor_obrigatorio(self):
        with self.assertRaises(IntegrityError):
            Publicacao.objects.create(
                titulo="Sem autor", slug="sem-autor", conteudo="..."
            )

    def test_publicacao_sem_categoria(self):
        self.assertIsNone(self.publicacao.categoria)

    def test_publicacao_com_categoria(self):
        cat = Categoria.objects.create(nome="Dev", slug="dev")
        self.publicacao.categoria = cat
        self.publicacao.save()
        self.assertEqual(self.publicacao.categoria, cat)

    def test_delete_categoria_set_null(self):
        cat = Categoria.objects.create(nome="X", slug="x")
        self.publicacao.categoria = cat
        self.publicacao.save()
        cat.delete()
        self.publicacao.refresh_from_db()
        self.assertIsNone(self.publicacao.categoria)

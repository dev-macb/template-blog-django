from django.db import IntegrityError

from ..models import Publicacao
from .test_base import BaseTeste


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

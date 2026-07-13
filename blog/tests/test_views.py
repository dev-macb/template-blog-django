from django.urls import reverse

from ..models import Publicacao
from .test_base import BaseTeste


class PaginaInicialVisaoTeste(BaseTeste):
    def setUp(self):
        super().setUp()
        for i in range(5):
            Publicacao.objects.create(
                titulo=f"Post {i}",
                slug=f"post-{i}",
                conteudo="Conteúdo",
                autor=self.autor,
            )

    def test_codigo_status_200(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertEqual(resposta.status_code, 200)

    def test_template_usado(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertTemplateUsed(resposta, "blog/pagina_inicial.html")

    def test_contexto_tem_publicacoes(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertIn("publicacoes", resposta.context)

    def test_contexto_tem_publicacoes_destaque(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertIn("publicacoes_destaque", resposta.context)

    def test_destaques_ordenados_por_visualizacoes(self):
        for i, visitas in enumerate([0, 10, 5, 3, 8]):
            Publicacao.objects.create(
                titulo=f"Views {i}",
                slug=f"views-{i}",
                conteudo="...",
                autor=self.autor,
                visualizacoes=visitas,
            )
        resposta = self.client.get(reverse("pagina_inicial"))
        destaques = resposta.context["publicacoes_destaque"]
        self.assertEqual(len(destaques), 3)
        self.assertEqual(destaques[0].slug, "views-1")
        self.assertEqual(destaques[1].slug, "views-4")
        self.assertEqual(destaques[2].slug, "views-2")


class PaginaInicialVaziaTeste(BaseTeste):
    def setUp(self):
        pass

    def test_lista_vazia_retorna_200(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertEqual(resposta.status_code, 200)

    def test_lista_vazia_sem_publicacoes(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertQuerySetEqual(resposta.context["publicacoes"], [])

    def test_lista_vazia_sem_destaques(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertQuerySetEqual(resposta.context["publicacoes_destaque"], [])


class DetalhePublicacaoVisaoTeste(BaseTeste):
    def test_codigo_status_200(self):
        resposta = self.client.get(
            reverse("detalhe_publicacao", args=["teste"])
        )
        self.assertEqual(resposta.status_code, 200)

    def test_404_para_slug_invalido(self):
        resposta = self.client.get(
            reverse("detalhe_publicacao", args=["slug-inexistente"])
        )
        self.assertEqual(resposta.status_code, 404)

    def test_contexto_tem_publicacao(self):
        resposta = self.client.get(
            reverse("detalhe_publicacao", args=["teste"])
        )
        self.assertEqual(resposta.context["publicacao"], self.publicacao)

    def test_incrementa_visualizacoes_uma_visita(self):
        self.client.get(reverse("detalhe_publicacao", args=["teste"]))
        self.publicacao.refresh_from_db()
        self.assertEqual(self.publicacao.visualizacoes, 1)

    def test_incrementa_visualizacoes_multiplas_visitas(self):
        for _ in range(5):
            self.client.get(reverse("detalhe_publicacao", args=["teste"]))
        self.publicacao.refresh_from_db()
        self.assertEqual(self.publicacao.visualizacoes, 5)

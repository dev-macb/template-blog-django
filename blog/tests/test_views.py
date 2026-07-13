from django.urls import reverse

from ..models import Categoria, Publicacao
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

    def test_contexto_tem_categorias(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertIn("categorias", resposta.context)

    def test_contexto_categorias_selecionadas_vazia(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertEqual(resposta.context["categorias_selecionadas"], [])

    def test_contexto_termo_busca_vazio(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertEqual(resposta.context["termo_busca"], "")

    def test_destaques_nao_sao_afetados_por_filtro_categoria(self):
        cat = Categoria.objects.create(nome="Tech", slug="tech")
        self.publicacao.categoria = cat
        self.publicacao.save()
        self.publicacao.refresh_from_db()
        for i in range(5):
            Publicacao.objects.create(
                titulo=f"Alto {i}",
                slug=f"alto-{i}",
                conteudo="...",
                autor=self.autor,
                visualizacoes=100 + i,
            )
        resposta = self.client.get(reverse("pagina_inicial") + "?categorias=tech")
        destaques = resposta.context["publicacoes_destaque"]
        self.assertEqual(destaques.count(), 3)
        titulos_destaques = [d.titulo for d in destaques]
        self.assertIn(f"Alto {4}", titulos_destaques)
        self.assertIn(f"Alto {3}", titulos_destaques)
        self.assertIn(f"Alto {2}", titulos_destaques)


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


class FiltroCategoriaVisaoTeste(BaseTeste):
    def setUp(self):
        super().setUp()
        self.categoria = Categoria.objects.create(nome="Tech", slug="tech")
        self.publicacao.categoria = self.categoria
        self.publicacao.save()
        self.pub2 = Publicacao.objects.create(
            titulo="Sem categoria",
            slug="sem-categoria",
            conteudo="...",
            autor=self.autor,
        )

    def test_filtro_por_categoria(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?categorias=tech")
        self.assertEqual(resposta.status_code, 200)
        publicacoes_listagem = list(resposta.context["publicacoes"])
        titulos = [p.titulo for p in publicacoes_listagem]
        self.assertIn(self.publicacao.titulo, titulos)

    def test_filtro_oculta_posts_outras_categorias_na_listagem(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?categorias=tech")
        publicacoes_listagem = list(resposta.context["publicacoes"])
        titulos_listagem = [p.titulo for p in publicacoes_listagem]
        self.assertIn(self.publicacao.titulo, titulos_listagem)
        self.assertNotIn(self.pub2.titulo, titulos_listagem)

    def test_categoria_inexistente_retorna_lista_vazia(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?categorias=naoexiste")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context["publicacoes"]), 0)

    def test_sem_filtro_mostra_todos(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, self.publicacao.titulo)
        self.assertContains(resposta, self.pub2.titulo)

    def test_categorias_selecionadas_no_contexto(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?categorias=tech")
        self.assertEqual(resposta.context["categorias_selecionadas"], ["tech"])

    def test_categorias_no_contexto(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertIn(self.categoria, resposta.context["categorias"])

    def test_multiplas_categorias(self):
        cat2 = Categoria.objects.create(nome="Design", slug="design")
        pub3 = Publicacao.objects.create(
            titulo="Post Design",
            slug="post-design",
            conteudo="...",
            autor=self.autor,
            categoria=cat2,
        )
        resposta = self.client.get(
            reverse("pagina_inicial") + "?categorias=tech&categorias=design"
        )
        publicacoes_listagem = list(resposta.context["publicacoes"])
        titulos = [p.titulo for p in publicacoes_listagem]
        self.assertIn(self.publicacao.titulo, titulos)
        self.assertIn(pub3.titulo, titulos)
        self.assertNotIn(self.pub2.titulo, titulos)
        self.assertEqual(len(resposta.context["categorias_selecionadas"]), 2)


class BuscaTituloVisaoTeste(BaseTeste):
    def setUp(self):
        super().setUp()
        Publicacao.objects.create(
            titulo="Python avançado",
            slug="python-avancado",
            conteudo="...",
            autor=self.autor,
        )
        Publicacao.objects.create(
            titulo="Django para iniciantes",
            slug="django-iniciantes",
            conteudo="...",
            autor=self.autor,
        )
        Publicacao.objects.create(
            titulo="JavaScript moderno",
            slug="javascript-moderno",
            conteudo="...",
            autor=self.autor,
        )

    def test_busca_por_titulo(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?titulo=python")
        publicacoes_listagem = list(resposta.context["publicacoes"])
        titulos_listagem = [p.titulo for p in publicacoes_listagem]
        self.assertIn("Python avançado", titulos_listagem)
        self.assertNotIn("JavaScript moderno", titulos_listagem)
        self.assertNotIn("Django para iniciantes", titulos_listagem)

    def test_busca_case_insensitivo(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?titulo=DJANGO")
        self.assertContains(resposta, "Django para iniciantes")

    def test_busca_vazia_mostra_todos(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?titulo=")
        self.assertContains(resposta, "Python avançado")
        self.assertContains(resposta, "Django para iniciantes")
        self.assertContains(resposta, "JavaScript moderno")

    def test_busca_termo_no_contexto(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?titulo=django")
        self.assertEqual(resposta.context["termo_busca"], "django")

    def test_busca_preserva_filtro_categoria(self):
        cat = Categoria.objects.create(nome="Backend", slug="backend")
        self.publicacao.categoria = cat
        self.publicacao.save()
        resposta = self.client.get(
            reverse("pagina_inicial") + "?categorias=backend&titulo=Teste"
        )
        self.assertEqual(resposta.context["categorias_selecionadas"], ["backend"])
        self.assertEqual(resposta.context["termo_busca"], "Teste")
        self.assertContains(resposta, self.publicacao.titulo)

    def test_busca_nao_encontrada(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?titulo=xyz123")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context["publicacoes"]), 0)

    def test_paginacao_preserva_busca(self):
        for i in range(25):
            Publicacao.objects.create(
                titulo=f"Post busca {i}",
                slug=f"post-busca-{i}",
                conteudo="...",
                autor=self.autor,
            )
        resposta = self.client.get(
            reverse("pagina_inicial") + "?titulo=post&pagina=2"
        )
        self.assertEqual(resposta.context["termo_busca"], "post")
        self.assertTrue(resposta.context["publicacoes"].has_next())


class PaginacaoVisaoTeste(BaseTeste):
    def setUp(self):
        super().setUp()
        for i in range(15):
            Publicacao.objects.create(
                titulo=f"Post {i}",
                slug=f"post-{i}",
                conteudo="...",
                autor=self.autor,
            )

    def test_primeira_pagina_tem_10_posts(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertEqual(len(resposta.context["publicacoes"]), 10)

    def test_segunda_pagina_tem_posts_restantes(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?pagina=2")
        self.assertEqual(len(resposta.context["publicacoes"]), 6)

    def test_pagina_invalida_retorna_primeira(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?pagina=abc")
        self.assertEqual(resposta.context["publicacoes"].number, 1)

    def test_pagina_acima_do_total_retorna_ultima(self):
        resposta = self.client.get(reverse("pagina_inicial") + "?pagina=999")
        self.assertEqual(resposta.context["publicacoes"].number, 2)

    def test_paginacao_preserva_filtro_categoria(self):
        cat = Categoria.objects.create(nome="X", slug="x")
        for i in range(12):
            Publicacao.objects.create(
                titulo=f"Cat {i}",
                slug=f"cat-{i}",
                conteudo="...",
                autor=self.autor,
                categoria=cat,
            )
        resposta = self.client.get(
            reverse("pagina_inicial") + "?categorias=x&pagina=2"
        )
        self.assertEqual(len(resposta.context["publicacoes"]), 2)
        self.assertEqual(resposta.context["categorias_selecionadas"], ["x"])

    def test_template_renderiza_paginacao(self):
        resposta = self.client.get(reverse("pagina_inicial"))
        self.assertContains(resposta, "class=\"paginacao\"")


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

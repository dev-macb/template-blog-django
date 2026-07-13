from django.contrib.auth.models import Permission
from django.urls import reverse

from ..models import Publicacao
from .test_base import BaseTeste


class PublicacaoAdminTeste(BaseTeste):
    def setUp(self):
        super().setUp()

        permissoes = Permission.objects.filter(
            content_type__app_label="blog",
            codename__in=[
                "add_publicacao",
                "change_publicacao",
                "delete_publicacao",
                "view_publicacao",
            ],
        )
        self.autor.user_permissions.add(*permissoes)

        self.outra = Publicacao.objects.create(
            titulo="Post de outro",
            slug="post-de-outro",
            conteudo="...",
            autor=self.administrador,
        )

        self.url_lista_alteracao = reverse("admin:blog_publicacao_changelist")
        self.url_adicionar = reverse("admin:blog_publicacao_add")

    def test_admin_lista_todas_para_super_usuario(self):
        self.client.force_login(self.administrador)
        resposta = self.client.get(self.url_lista_alteracao)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context["cl"].queryset), 2)

    def test_admin_lista_somente_do_autor_para_escritor(self):
        self.client.force_login(self.autor)
        resposta = self.client.get(self.url_lista_alteracao)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context["cl"].queryset), 1)

    def test_admin_save_model_atribui_autor_automaticamente(self):
        self.client.force_login(self.autor)
        resposta = self.client.post(self.url_adicionar, {
            "titulo": "Novo Post",
            "slug": "novo-post",
            "conteudo": "<p>HTML</p>",
            "visualizacoes": "0",
            "_save": "1",
        }, follow=True)
        self.assertEqual(resposta.status_code, 200)
        if resposta.context and resposta.context.get("adminform"):
            self.fail(f"Erros no formulário: {resposta.context['adminform'].form.errors}")
        publicacao = Publicacao.objects.get(slug="novo-post")
        self.assertEqual(publicacao.autor, self.autor)

    def test_admin_oculta_campo_autor_para_escritor(self):
        self.client.force_login(self.autor)
        resposta = self.client.get(self.url_adicionar)
        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn("autor", resposta.context["adminform"].form.fields)

    def test_admin_mostra_campo_autor_para_super_usuario(self):
        self.client.force_login(self.administrador)
        resposta = self.client.get(self.url_adicionar)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("autor", resposta.context["adminform"].form.fields)

    def test_admin_busca_por_titulo(self):
        self.client.force_login(self.administrador)
        resposta = self.client.get(self.url_lista_alteracao, {"q": "Teste"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context["cl"].queryset), 1)

    def test_admin_busca_por_conteudo(self):
        self.client.force_login(self.administrador)
        resposta = self.client.get(self.url_lista_alteracao, {"q": "HTML"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context["cl"].queryset), 1)

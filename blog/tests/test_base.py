from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Publicacao


class BaseTeste(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user(
            username="autor", password="123", is_staff=True
        )
        self.administrador = User.objects.create_user(
            username="administrador", password="123", is_staff=True, is_superuser=True
        )
        self.publicacao = Publicacao.objects.create(
            titulo="Teste",
            slug="teste",
            conteudo="<p>Conteúdo HTML</p>",
            autor=self.autor,
        )

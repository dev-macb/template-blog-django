from django.template import Context, Template
from django.test import TestCase
from django.utils.safestring import SafeString


class FiltroMarkdownTeste(TestCase):
    def test_retorna_string_segura(self):
        modelo = Template("{% load extras_markdown %}{{ valor|markdown }}")
        resultado = modelo.render(Context({"valor": "<b>HTML</b>"}))
        self.assertIsInstance(resultado, SafeString)

    def test_nao_escapa_html(self):
        modelo = Template("{% load extras_markdown %}{{ valor|markdown }}")
        resultado = modelo.render(Context({"valor": "<strong>negrito</strong>"}))
        self.assertInHTML("<strong>negrito</strong>", resultado)

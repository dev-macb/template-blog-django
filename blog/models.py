from django.contrib.auth.models import User
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Publicacao(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subtitulo = models.CharField(max_length=300, blank=True)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to="publicacoes/", blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    visualizacoes = models.IntegerField(default=0, db_index=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publicacoes",
    )

    class Meta:
        ordering = ["-data_criacao"]
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"

    def __str__(self):
        return self.titulo

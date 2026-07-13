from django.contrib.auth.models import User
from django.db import models


class Publicacao(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subtitulo = models.CharField(max_length=300, blank=True)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to="publicacoes/", blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    visualizacoes = models.IntegerField(default=0, db_index=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-data_criacao"]
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"

    def __str__(self):
        return self.titulo

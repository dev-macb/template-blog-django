from django.contrib import admin

from .models import Publicacao


@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'subtitulo', 'autor', 'data_criacao')
    search_fields = ('titulo', 'conteudo')
    prepopulated_fields = {'slug': ('titulo',)}

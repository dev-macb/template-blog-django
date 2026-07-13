from django.contrib import admin
from .models import Categoria, Publicacao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome",)


@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo", "slug", "subtitulo", "autor", "categoria",
        "data_criacao", "visualizacoes",
    )
    list_filter = ("data_criacao", "categoria")
    search_fields = ("titulo", "conteudo")
    prepopulated_fields = {"slug": ("titulo",)}

    def get_queryset(self, request):
        consulta = super().get_queryset(request)
        if request.user.is_superuser:
            return consulta
        return consulta.filter(autor=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and "autor" in form.base_fields:
            del form.base_fields["autor"]
        return form

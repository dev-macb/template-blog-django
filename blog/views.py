from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from .models import Categoria, Publicacao


def pagina_inicial(request):
    publicacoes_destaque = Publicacao.objects.order_by("-visualizacoes")[:3]

    publicacoes = Publicacao.objects.all().select_related("autor", "categoria")

    categorias_selecionadas = request.GET.getlist("categorias")
    if categorias_selecionadas:
        publicacoes = publicacoes.filter(categoria__slug__in=categorias_selecionadas)

    termo_busca = request.GET.get("titulo", "").strip()
    if termo_busca:
        publicacoes = publicacoes.filter(titulo__icontains=termo_busca)

    paginator = Paginator(publicacoes, 10)
    numero_pagina = request.GET.get("pagina")
    publicacoes_paginadas = paginator.get_page(numero_pagina)

    return render(
        request,
        "blog/pagina_inicial.html",
        {
            "publicacoes_destaque": publicacoes_destaque,
            "publicacoes": publicacoes_paginadas,
            "categorias": Categoria.objects.all(),
            "categorias_selecionadas": categorias_selecionadas,
            "termo_busca": termo_busca,
        },
    )


def detalhe_publicacao(request, slug):
    publicacao = get_object_or_404(
        Publicacao.objects.select_related("autor", "categoria"), slug=slug
    )
    Publicacao.objects.filter(pk=publicacao.pk).update(visualizacoes=F("visualizacoes") + 1)
    publicacao.refresh_from_db(fields=["visualizacoes"])
    return render(request, "blog/detalhe_publicacao.html", {"publicacao": publicacao})

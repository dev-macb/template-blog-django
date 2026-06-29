from django.db.models import F
from django.shortcuts import get_object_or_404, render

from .models import Publicacao


def pagina_inicial(request):
    publicacoes_destaque = Publicacao.objects.order_by('-visualizacoes')[:3]
    publicacoes = Publicacao.objects.all().select_related('autor')
    return render(request, 'blog/pagina_inicial.html', {
        'publicacoes_destaque': publicacoes_destaque,
        'publicacoes': publicacoes,
    })


def detalhe_publicacao(request, slug):
    publicacao = get_object_or_404(Publicacao.objects.select_related('autor'), slug=slug)
    Publicacao.objects.filter(pk=publicacao.pk).update(visualizacoes=F('visualizacoes') + 1)
    publicacao.refresh_from_db(fields=['visualizacoes'])
    return render(request, 'blog/detalhe_publicacao.html', {'publicacao': publicacao})

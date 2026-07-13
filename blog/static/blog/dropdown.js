(function () {
    var botao = document.getElementById('botao-categorias');
    var painel = document.getElementById('painel-categorias');
    var dropdown = document.getElementById('dropdown-categorias');
    var form = document.getElementById('form-filtros');

    if (!botao || !painel) return;

    botao.addEventListener('click', function (e) {
        e.stopPropagation();
        painel.classList.toggle('aberto');
    });

    document.addEventListener('click', function (e) {
        if (!dropdown.contains(e.target)) {
            painel.classList.remove('aberto');
        }
    });

    var checkboxes = painel.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].addEventListener('change', function () {
            form.submit();
        });
    }
})();

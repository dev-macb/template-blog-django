# modelo-blog-django

Um blog desenvolvido com Django, com sistema de publicações, categorias, busca por título e paginação. O painel administrativo permite o gerenciamento completo dos posts, com controle de acesso para administradores e escritores.


## Instalação

```bash
pip install -r requirements.txt
```


## Configuração

Copie o arquivo `.env` e ajuste as variáveis:

```bash
cp .env.example .env
```


## Execução

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse:
- http://localhost:8000 — página inicial do blog
- http://localhost:8000/{ADMIN_URL}/ — painel administrativo


## Perfis de Usuário

| Perfil | Acesso | Como criar |
|---|---|---|
| **Administrador** | Acesso total ao admin | `python manage.py createsuperuser` |
| **Escritor** | Admin apenas para gerenciar publicações (somente as próprias) | Criar usuário pelo admin: **Staff** + grupo **Escritores** |

O grupo **Escritores** é criado automaticamente pela migration com permissões de adicionar, editar, excluir e visualizar publicações.

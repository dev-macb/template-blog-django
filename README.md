# template-blog-django

Um simples template de blog construído com Django.

## Requisitos

- Python 3.14+
- Django 6.0+

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Copie o arquivo `.env` e ajuste as variáveis:

```bash
cp .env .env.local
```

### Variáveis de ambiente

| Variável | Descrição | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django | **obrigatório** |
| `DEBUG` | Modo de desenvolvimento | `False` |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por vírgula) | `localhost,127.0.0.1` |
| `CSRF_TRUSTED_ORIGINS` | Origens confiáveis para CSRF | `""` |
| `ADMIN_URL` | Caminho do painel admin | `admin` |
| `SECURE_SSL_REDIRECT` | Redirecionar HTTP para HTTPS | `True` (desliga com `DEBUG=True`) |
| `SECURE_HSTS_SECONDS` | Tempo de HSTS em segundos | `0` |
| `SESSION_COOKIE_SECURE` | Cookie de sessão apenas via HTTPS | `True` (desliga com `DEBUG=True`) |
| `CSRF_COOKIE_SECURE` | Cookie CSRF apenas via HTTPS | `True` (desliga com `DEBUG=True`) |

### Segurança

- `ADMIN_URL` permite ocultar o painel admin em um caminho personalizado
- `SESSION_COOKIE_HTTPONLY` e `CSRF_COOKIE_HTTPONLY` bloqueiam acesso JS aos cookies
- `SECURE_REFERRER_POLICY=same-origin` restringe o header Referer
- `SECURE_PROXY_SSL_HEADER` configurado para reverse proxy (nginx, ELB, etc.)
- Markdown sanitizado com `bleach` (XSS prevention)
- `DATA_UPLOAD_MAX_MEMORY_SIZE` limitado a 5MB

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

## Funcionalidades

- Publicações com título, slug, subtítulo, conteúdo (Markdown), imagem e autor
- Contador de visualizações atômico (sem race condition)
- Seção de destaques (posts mais acessados)
- Preview de 200 caracteres na listagem
- Markdown com sanitização (bleach)
- Design responsivo sem frameworks CSS
- Testes automatizados (model + views)
- Configuração por variáveis de ambiente (python-decouple)
- Dois perfis de acesso: administrador e escritor

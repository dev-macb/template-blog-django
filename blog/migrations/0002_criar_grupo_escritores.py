from django.db import migrations


def criar_grupo_escritores(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Publicacao = apps.get_model('blog', 'Publicacao')

    content_type = ContentType.objects.get_for_model(Publicacao)
    permissoes = Permission.objects.filter(
        content_type=content_type,
        codename__in=['add_publicacao', 'change_publicacao', 'delete_publicacao', 'view_publicacao'],
    )

    grupo, _ = Group.objects.get_or_create(name='Escritores')
    grupo.permissions.set(permissoes)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_grupo_escritores),
    ]

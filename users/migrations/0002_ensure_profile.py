from django.db import migrations

def forwards_func(apps, schema_editor):
    # Pular a criação da tabela via SQL bruto
    # Em vez disso, vamos apenas criar perfis para usuários existentes
    CustomUser = apps.get_model("users", "CustomUser")
    Profile = apps.get_model("users", "Profile")
    
    db_alias = schema_editor.connection.alias
    for user in CustomUser.objects.using(db_alias).all():
        try:
            Profile.objects.using(db_alias).get(user=user)
        except Profile.DoesNotExist:
            Profile.objects.using(db_alias).create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]

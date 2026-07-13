# Generated manually

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_rename_seat_type_seat_type_alter_train_train_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seat',
            options={'verbose_name': '座位', 'verbose_name_plural': '座位'},
        ),
        migrations.AlterModelOptions(
            name='train',
            options={'verbose_name': '列车', 'verbose_name_plural': '列车'},
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('train', 'type')},
        ),
    ]

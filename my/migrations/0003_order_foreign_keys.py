# Generated manually for Order model refactor

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def migrate_order_foreign_keys(apps, schema_editor):
    """将旧订单中的车次号/座位中文名迁移为外键关联"""
    Order = apps.get_model('my', 'Order')
    Train = apps.get_model('ticket', 'Train')
    Seat = apps.get_model('ticket', 'Seat')

    seat_type_map = {
        '商务座': 'business',
        '一等座': 'first',
        '二等座': 'second',
        'business': 'business',
        'first': 'first',
        'second': 'second',
    }

    for order in Order.objects.all():
        train_number = getattr(order, 'train_number', None)
        seat_type_label = getattr(order, 'seat_type', None)
        if not train_number:
            continue
        try:
            train = Train.objects.get(number=train_number)
            seat_code = seat_type_map.get(seat_type_label, seat_type_label)
            seat = Seat.objects.get(train=train, type=seat_code)
            order.train = train
            order.seat = seat
            order.save(update_fields=['train', 'seat'])
        except (Train.DoesNotExist, Seat.DoesNotExist):
            # 无法关联的历史脏数据直接删除
            order.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_rename_seat_type_seat_type_alter_train_train_type'),
        ('my', '0002_delete_userinfo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='train',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='ticket.train',
                verbose_name='车次',
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='seat',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='ticket.seat',
                verbose_name='座位',
            ),
        ),
        migrations.RunPython(migrate_order_foreign_keys, migrations.RunPython.noop),
        migrations.RemoveField(model_name='order', name='train_number'),
        migrations.RemoveField(model_name='order', name='seat_type'),
        migrations.AlterField(
            model_name='order',
            name='train',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='ticket.train',
                verbose_name='车次',
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='seat',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='ticket.seat',
                verbose_name='座位',
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='成交价格'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='购买时间'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='orders',
                to=settings.AUTH_USER_MODEL,
                verbose_name='用户',
            ),
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': '订单', 'verbose_name_plural': '订单'},
        ),
    ]

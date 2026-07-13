from django.db import models


class Train(models.Model):
    """列车车次信息"""

    TRAIN_TYPES = [('G', '高铁'), ('D', '动车'), ('T', '特快')]

    number = models.CharField('车次', max_length=10, unique=True)
    train_type = models.CharField('类型', max_length=1, choices=TRAIN_TYPES)
    qi = models.CharField('出发地', max_length=50)
    mudi = models.CharField('目的地', max_length=50)
    start_time = models.DateTimeField('出发时间')
    end_time = models.DateTimeField('到达时间')

    class Meta:
        verbose_name = '列车'
        verbose_name_plural = '列车'

    def __str__(self):
        return f"{self.number} ({self.get_train_type_display()})"


class Seat(models.Model):
    """某车次下的座位类型及余票"""

    SEAT_TYPES = [
        ('business', '商务座'),
        ('first', '一等座'),
        ('second', '二等座'),
    ]

    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name='seats',
        verbose_name='所属车次',
    )
    type = models.CharField('座位类型', max_length=20, choices=SEAT_TYPES)
    price = models.DecimalField('价格', max_digits=7, decimal_places=2)
    number = models.PositiveIntegerField('剩余票数', default=100)

    class Meta:
        verbose_name = '座位'
        verbose_name_plural = '座位'
        # 同一车次下每种座位类型唯一
        unique_together = [('train', 'type')]

    def __str__(self):
        return f"{self.train.number} - {self.get_type_display()} ({self.price}元)"

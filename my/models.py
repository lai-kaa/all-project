from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    """
    用户购票订单。
    通过外键关联 Train / Seat，避免仅存字符串导致退票时映射失败。
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='用户',
    )
    train = models.ForeignKey(
        'ticket.Train',
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='车次',
    )
    seat = models.ForeignKey(
        'ticket.Seat',
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='座位',
    )
    # 下单时快照价格，防止后续调价影响历史订单
    price = models.DecimalField('成交价格', max_digits=7, decimal_places=2)
    created_at = models.DateTimeField('购买时间', auto_now_add=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.train.number} - {self.seat.get_type_display()}"

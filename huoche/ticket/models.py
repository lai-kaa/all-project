from django.db import models

class Train(models.Model):
    TRAIN_TYPES = [('G','高铁'),('D','动车'),('T','特快')]
    number   = models.CharField('车次', max_length=10, unique=True)
    train_type = models.CharField('类型', max_length=1, choices=TRAIN_TYPES)
    qi       = models.CharField('出发地', max_length=50)
    mudi     = models.CharField('目的地', max_length=50)
    start_time = models.DateTimeField('出发时间')
    end_time   = models.DateTimeField('到达时间')

    def __str__(self):
        return f"{self.number} ({self.get_train_type_display()})"

class Seat(models.Model):
    SEAT_TYPES = [('business','商务座'),('first','一等座'),('second','二等座')]
    train  = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='seats')
    type   = models.CharField('座位类型', max_length=20, choices=SEAT_TYPES)
    price  = models.DecimalField('价格', max_digits=7, decimal_places=2)
    number = models.PositiveIntegerField('剩余票数', default=100)

    def __str__(self):
        return f"{self.train.number} - {self.get_type_display()} ({self.price}元)"
    

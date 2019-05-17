from django.db import models

# Create your models here.
from goods.models import Goods
from user.models import AXFUser


class Cart(models.Model):
    c_user = models.ForeignKey(AXFUser,related_name='ca',on_delete=models.CASCADE)
    c_goods = models.ForeignKey(Goods,related_name='ct',on_delete=models.CASCADE)

    c_goods_num = models.IntegerField(default=1)
    c_is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'cart'



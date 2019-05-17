
from rest_framework.routers import SimpleRouter

from carts.views import *

router=SimpleRouter()

router.register('cart',CartView)

urlpatterns=[

]

urlpatterns+=router.urls

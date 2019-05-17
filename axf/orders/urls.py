from django.urls import path

from  rest_framework.routers import SimpleRouter

# from orders.views import OrderView
from orders.views import orders

router=SimpleRouter()

# router.register('orders',OrderView)
urlpatterns =[
   path('orders/',orders)
]

urlpatterns+=router.urls

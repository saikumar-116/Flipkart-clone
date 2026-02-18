from django.contrib import admin
from .models import (
    Product, Order, OrderItem,
    LifeEvent, EventProduct,
    GroupDeal, GroupDealMember
)

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(LifeEvent)
admin.site.register(EventProduct)
admin.site.register(GroupDeal)
admin.site.register(GroupDealMember)

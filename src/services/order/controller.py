"""order controller file"""
from src.config.error_constants import ErrorMessage
from src.services.order.model import OrderModel
from src.services.order.serializers import OrderInbound, OrderSaveInbound, OrderSaveOutbound, UpdateOrderInbound
from src.services.order_items.model import OrderItemsModel
from src.services.order_items.serializers import OrderItemInbound
from src.utils.common_serializers import CommonMessageOutbound


class OrdersController:
    """order controller class"""

    @staticmethod
    async def create_orders(cls):
        """create orders"""
        total_amount = 0
        all_order_items = []
        order = OrderSaveInbound(**payload.__dict__)
        order = OrderModel.create(**order.__dict__)
        for item in payload.items or []:
            total_amount += item.price * item.quantity
            order_item = OrderItemInbound(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=item.price)
            order_item = OrderItemsModel.create(**order_item.__dict__)
            all_order_items.append(order_item)
        order = OrderModel.patch(_id=order.id, **{"total": total_amount})
        result = OrderSaveOutbound(
            id=order.id,
            user_id=order.user_id,
            total_amount=order.total,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=all_order_items,
            status=order.status
        )
        return CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=result.__dict__)

    @classmethod
    async def update_orders(cls, payload: UpdateOrderInbound):
        """update orders"""
        total_amount = 0
        order = OrderModel.get(_id=payload.id)
        if not order:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        all_order_items = []
        for item in payload.items or []:
            order_item = OrderItemsModel.get(_id=item.id)
            if not order_item:
                return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
            total_amount += item.price * item.quantity
            order_item = OrderItemInbound(order_id=order.id, product_id=item.product_id, quantity=item.quantity,price=item.price)
            order_item = OrderItemsModel.patch(_id=item.id, **order_item.__dict__)
            all_order_items.append(order_item)
        order = OrderModel.patch(_id=order.id, **{"total": total_amount})
        result = OrderSaveOutbound(
            id=order.id,
            user_id=order.user_id,
            total_amount=order.total,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=all_order_items,
            status=order.status
        )
        return CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=result.__dict__)

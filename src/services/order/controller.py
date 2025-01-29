"""order controller file"""
from src.config.constants import OrderStatusConstant
from src.config.error_constants import ErrorMessage
from src.services.order.model import OrderModel
from src.services.order.serializers import OrderInbound, OrderSaveInbound, OrderSaveOutbound, UpdateOrderInbound
from src.services.order_items.model import OrderItemsModel
from src.services.order_items.serializers import OrderItemOutbound, OrderItemFinalInbound
from src.services.product.controller import ProductController
from src.services.product.model import ProductModel
from src.services.product.serializers import ProductOutBound
from src.services.user.controller import user_details_context
from src.utils.common_serializers import CommonMessageOutbound


class OrdersController:
    """order controller class"""

    @classmethod
    async def save(cls, payload: OrderInbound):
        """create orders"""
        user_data = user_details_context.get()
        total_amount = 0
        all_order_items = []
        order = OrderSaveInbound(**{"user_id": user_data.id, "total": total_amount})
        order = OrderModel.create(**order.__dict__)
        for item in payload.items or []:
            product_data = await ProductController.get_product(_id=item.product_id)
            if not product_data.data:
                OrderModel.delete(_id=order.id)
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("product_id"))))
            if product_data.data.get("stock") < item.quantity:
                OrderModel.delete(_id=order.id)
                return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.STOCKS_NOT_AVAILABLE)))
            total_amount += product_data.data.get("price") * item.quantity
            order_item = OrderItemFinalInbound(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=product_data.data.get("price"))
            order_item = OrderItemsModel.create(**order_item.__dict__)
            all_order_items.append(OrderItemOutbound(
                id=order_item.id,
                product=ProductOutBound(**product_data.data),
                quantity=order_item.quantity
            ))
            remaining_stock = abs(product_data.data.get("stock", 0) - item.quantity)
            ProductModel.patch(_id=item.product_id, **{"stock": remaining_stock})
        order = OrderModel.patch(_id=order.id, **{"total": total_amount})
        result = OrderSaveOutbound(
            id=order.id,
            user=user_data,
            total_amount=order.total,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=all_order_items,
            status=order.status
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=result.__dict__)))

    @classmethod
    async def update_orders(cls, payload: UpdateOrderInbound):
        """update orders"""
        user_data = user_details_context.get()
        total_amount = 0
        order = OrderModel.get(_id=payload.id, user_id=user_data.id, status=[OrderStatusConstant.Placed])
        if not order:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
        all_order_items = []
        for item in payload.items or []:
            order_item = OrderItemsModel.get(_id=item.id)
            if not order_item:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
            product_data = await ProductController.get_product(_id=order_item.product_id)
            if not product_data.data:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("product_id"))))
            if product_data.data.get("stock") < item.quantity:
                return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.STOCKS_NOT_AVAILABLE)))
            total_amount += product_data.data.get("price", 0) * item.quantity
            order_item = OrderItemFinalInbound(order_id=order.id, product_id=product_data.data.get("id"), quantity=item.quantity,price=product_data.data.get("price", 0))
            order_item = OrderItemsModel.patch(_id=item.id, **order_item.__dict__)
            all_order_items.append(OrderItemOutbound(
                id=order_item.id,
                product=product_data.data,
                quantity=order_item.quantity
            ))
            remaining_stock = abs(product_data.data.get("stock", 0) - item.quantity)
            ProductModel.patch(_id=product_data.data.get("id"), **{"stock": remaining_stock})
        order = OrderModel.patch(_id=order.id, **{"total": total_amount})
        result = OrderSaveOutbound(
            id=order.id,
            user=user_data,
            total_amount=order.total,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=all_order_items,
            status=order.status
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=result.__dict__)))

    @classmethod
    async def get(cls, _id: int = None, page: int = 1, size: int = 10):
        """get orders"""
        user_data = user_details_context.get()
        order = OrderModel.get(_id=_id, user_id=user_data.id, page=page, size=size)
        if not order:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
        items_data = []
        if _id:
            order_item = OrderItemsModel.get(order_id=order.id)
            for item in order_item or []:
                product = await ProductController.get_product(_id=item.product_id)
                items_data.append(
                    OrderItemOutbound(
                        id=item.id,
                        product=product.data,
                        quantity=item.quantity
                    )
                )
            data = OrderSaveOutbound(
                id=order.id,
                user=user_data,
                total_amount=order.total,
                created_at=order.created_at,
                updated_at=order.updated_at,
                status=order.status,
                items=items_data
                )
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.FETCH_SUCCESSFULLY, data=data.__dict__)))
        else:
            order_response = []
            for order_ in order or []:
                order_item = OrderItemsModel.get(order_id=order_.id)
                items_data = [] 
                for item in order_item or []:
                    product = await ProductController.get_product(_id=item.product_id)
                    items_data.append(
                        OrderItemOutbound(
                            id=item.id,
                            product=product.data,
                            quantity=item.quantity
                        )
                    )
                order_result = OrderSaveOutbound(
                        id=order_.id,
                        user=user_data,
                        total_amount=order_.total,
                        created_at=order_.created_at,
                        updated_at=order_.updated_at,
                        status=order_.status,
                        items=items_data
                    )
                order_response.append(order_result.__dict__)
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.FETCH_SUCCESSFULLY, data=order_response)))

    @classmethod
    async def delete(cls, _id: int):
        """delete orders"""
        user_data = user_details_context.get()
        order = OrderModel.get(_id=_id, user_id=user_data.id)
        if not order:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
        order_items = OrderItemsModel.get(order_id=_id)
        for order_item in order_items or []:
            item_ = OrderItemsModel.patch(_id=order_item.id, **{"status": OrderStatusConstant.Canceled})
            product = await ProductController.get_product(_id=item_.product_id)
            if not product.data:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
            quantity = product.data.get("stock", 0) + order_item.quantity
            ProductModel.patch(_id=item_.product_id, **{"stock": quantity})
        OrderModel.patch(_id=_id, **{"status": OrderStatusConstant.Canceled})
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY)))

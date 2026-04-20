from .models import Product

class InventoryService:
    @staticmethod
    def is_product_low_stock(product: Product) -> bool:
        return product.stock_on_hand <= product.reorder_level

    @staticmethod
    def adjust_stock(product: Product, quantity: int, increase: bool = True) -> Product:
        if quantity < 0:
            raise ValueError("Quantity must be non-negative.")

        if increase:
            product.stock_on_hand += quantity
        else:
            if quantity > product.stock_on_hand:
                raise ValueError("Cannot reduce stock below zero.")
            product.stock_on_hand -= quantity

        product.save(update_fields=["stock_on_hand", "updated_at"])
        return product
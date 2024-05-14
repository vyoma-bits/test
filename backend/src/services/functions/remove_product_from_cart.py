from tenacity import retry, stop_after_attempt, wait_fixed

@retry(wait=wait_fixed(1), stop=stop_after_attempt(5))
async def remove_product_from_cart(
        CONFIG,
        product_id: str=None,
        quantity: int=1,
):
    return {
        "response": {
            "product_id": str(product_id),
            "quantity": int(quantity)
        }
    }
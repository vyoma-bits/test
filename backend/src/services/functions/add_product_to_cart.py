from tenacity import retry, wait_random, stop_after_attempt

@retry(wait=wait_random(min=1, max=5), stop=stop_after_attempt(5))
async def add_product_to_cart(
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
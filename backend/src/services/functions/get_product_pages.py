# from src.utils import PineconeDBHandler
from src.handlers.pinecone_handler import PineconeDBHandler
from llama_index.vector_stores.types import ExactMatchFilter
from tenacity import retry, wait_random, stop_after_attempt

@retry(wait=wait_random(min=1, max=5), stop=stop_after_attempt(5))
async def get_product_pages(
        CONFIG,
        name_of_product=None,
        type_of_product=None,
        brand_requested=None,
        screen_size=None,
        specs=None,
        price=None,
        other_information=None,
        quantity=1,
    ):
    """Opens the product page"""

    # Loads the product page from pinecone
    # #debug 
    # print("name_of_product: ", name_of_product)

    index_name = "gcp-starter"

    PineconeDBHandler.get_instance(index_name, CONFIG)
    customQuery = PineconeDBHandler.transform_query(name_of_product, type_of_product, brand_requested, screen_size, specs, \
                                               price, other_information) # formats the query to be used in the pinecone db
    
    print("customQuery: ", customQuery) # debug
    response = PineconeDBHandler.make_query(
        index_name=index_name,
        query=customQuery
    )

    for i in range(len(response)):
        response[i] = response[i]['metadata']

    return response

def get_query(
        name_of_product: str=None,
        type_of_product: str="",
        other_information:str ="",
    ):
    """Returns the query for the product page"""
    name_of_product_query = f"""
    Name: {name_of_product}
    """ if name_of_product else ""

    type_of_product_query = f"""
    Type of product: {type_of_product}
    """ if type_of_product else ""

    other_information_query = f"""
    Other information: {other_information}
    """ if other_information else ""

    return name_of_product_query + type_of_product_query + other_information_query
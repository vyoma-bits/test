from pinecone import Pinecone
from openai import OpenAI
from src.config import CONFIG
from src.schemas.base_models import QueryMessage

class Embedder:
    client = OpenAI(api_key=CONFIG["openai"]["api_key"])

    @staticmethod
    def embed(text):
        return Embedder.client.embeddings.create(input=[text], model=CONFIG["openai"]["embedding_model"]).data[0].embedding


class PineconeDB:
    def __init__(self, index_name):
        self.index_name = index_name
        self.pc = Pinecone(api_key=CONFIG['pinecone']['api_key'])
        self.index = self.pc.Index(index_name)

    def make_query(self, query: str):
        # embed the query
        query_embedding = Embedder.embed(query)
        response = self.index.query(
            namespace=CONFIG["pinecone"]["namespace"],
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )

        #debug
        print(response)
        return response["matches"]

class PineconeDBHandler:
    '''Handles pineconedb related operations'''
    instances = dict()
    
    # check for instance before executing any method
    def validate_instance(func):
        def wrapper(index_name,*args, **kwargs):
            if index_name not in PineconeDBHandler.instances.keys():
                raise Exception("Instance not found")
            return func(index_name, *args, **kwargs)
        return wrapper

    @staticmethod
    def get_instance(index_name, CONFIG):
        if index_name not in PineconeDBHandler.instances.keys():
            PineconeDBHandler.instances[index_name] = PineconeDB(index_name)
        return PineconeDBHandler.instances[index_name]
    
    @staticmethod
    @validate_instance
    def make_query(index_name, query):
        return PineconeDBHandler.instances[index_name].make_query(query)
    
    @staticmethod
    def transform_query(name_of_product = None, type_of_product = None, brand_requested = None, screen_size = None, specs = None, price = None, other_information = None):
        '''Makes query in a formatted way to be used in the pinecone db as defined in the schema QueryMessage'''
        query = QueryMessage(
            id = "null",
            category = type_of_product,
            brand = brand_requested,
            model = name_of_product,
            screen = screen_size,
            specs = specs,
            price = price,
            other_information = other_information
        )

        # convert query to json
        return str(query)

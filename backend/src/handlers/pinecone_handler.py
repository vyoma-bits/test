import openai
import pinecone
from src.config import CONFIG
from src.schemas.base_models import QueryMessage

class Embedder:
    client = openai.OpenAI(api_key=CONFIG["openai"]["api_key"])

    @staticmethod
    def embed(text):
        client = openai.OpenAI(api_key=CONFIG["openai"]["api_key"])
        

        response =client.embeddings.create(input=[text], model=CONFIG["openai"]["embedding_model"]).data[0].embedding
        return response

class PineconeDB:
    def __init__(self, index_name):
        pinecone.init(api_key=CONFIG['pinecone']['api_key'])
        self.index = pinecone.Index(index_name)

    def make_query(self, query: str):
        query_embedding = Embedder.embed(query)
        response = self.index.query(
            namespace=CONFIG["pinecone"]["namespace"],
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )

        print(response)
        return response["matches"]

class PineconeDBHandler:
    instances = dict()

    def validate_instance(func):
        def wrapper(index_name, *args, **kwargs):
            if index_name not in PineconeDBHandler.instances.keys():
                raise Exception("Instance not found")
            return func(index_name, *args, **kwargs)
        return wrapper

    @staticmethod
    def get_instance(index_name):
        if index_name not in PineconeDBHandler.instances.keys():
            PineconeDBHandler.instances[index_name] = PineconeDB(index_name)
        return PineconeDBHandler.instances[index_name]

    @staticmethod
    @validate_instance
    def make_query(index_name, query):
        return PineconeDBHandler.instances[index_name].make_query(query)

    @staticmethod
    def transform_query(name_of_product=None, type_of_product=None, brand_requested=None, screen_size=None, specs=None, price=None, other_information=None):
        query = QueryMessage(
            id="null",
            category=type_of_product,
            brand=brand_requested,
            model=name_of_product,
            screen=screen_size,
            specs=specs,
            price=price,
            other_information=other_information
        )
        return str(query)
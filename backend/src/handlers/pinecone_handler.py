
from llama_index.vector_stores import PineconeVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index import VectorStoreIndex, Document, ServiceContext
from llama_index.retrievers import VectorIndexRetriever
from ..schemas.base_models import QueryMessage
import json


# avoid using this class
class PineconeDB:
    def __init__(self, index_name, CONFIG):
        self.index_name = index_name
        self.CONFIG = CONFIG

        self.vector_store = PineconeVectorStore(
            index_name=index_name,
            environment=CONFIG["pinecone"]["environment"],
        )

        self.vector_index = VectorStoreIndex.from_vector_store(
            vector_store = self.vector_store,
        )

        self.retriever = VectorIndexRetriever(index = self.vector_index, similarity_top_k=100)
        self.query_engine = self.vector_index.as_query_engine()

    def get_retriever(self):    
        return self.retriever
    
    def make_query(self, query: str):
        response = self.retriever.retrieve(query)
        # response = self.query_engine.query(query)
        print("response: ", response)
        return response

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
            PineconeDBHandler.instances[index_name] = PineconeDB(index_name, CONFIG)
        return PineconeDBHandler.instances[index_name]
    
    @staticmethod
    @validate_instance
    def get_retriever(index_name):
        return PineconeDBHandler.instances[index_name].get_retriever()
    
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
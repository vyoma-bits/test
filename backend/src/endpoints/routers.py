"""File containing root routes"""
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from fastapi import File, UploadFile
from fastapi.encoders import jsonable_encoder
import base64
import httpx
import asyncio
import copy
import json
import tempfile
from pathlib import Path
import openai
import traceback

# Schemas
from src.schemas import FunctionCall
from src.schemas import (
    ChatRequest,
    FunctionCall,
    AudioTranscriptRequest,
    AudioTTSRequest,
)
from src.handlers import MainHandler
from src.data.data_models import Restaurant, Foods

# Services
from src.services import openai_service, functions

# Data
from sqlalchemy.orm import Session
from src.data.data_utils import get_db
def ask_openai(question, context):
    prompt = f"{context}\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=50,
        stop=["\n"]
    )
    answer = response.choices[0].text.strip()
    return answer
from typing import List

class InputMessage:
  def __init__(self, role: str, content: str, name: str = None):
    self.role = role
    self.content = content
    self.name = name

def InputChatHistory(history: List[InputMessage]) -> str:
  user_messages = [message.content for message in history if message.role == 'user']
  if user_messages:
    return user_messages[0]
  else:
    return "No user messages found in the history."

def create_router(handler: MainHandler, CONFIG):
    router = APIRouter()
    client = handler.openai_client

    ## Question answering
    @router.post("/chat/send_message")
    async def send_message(prompt_request: ChatRequest):
        """Receives the chatlog from the user and answers"""
        history=prompt_request.query
        print(history.history)
        user_message =InputChatHistory(history.history)
        print(user_message)

        print("prompt_request")
        data = data={
    "products": [
        {
            "id": "1",
            "category": "Laptop",
            "brand": "Apple",
            "model": "MacBook Pro",
            "screen": {
                "size": "15 inch"
            },
            "specs": {
                "RAM": "8GB",
                "processor": "Apple M1",
                "storage": "256GB SSD"
            },
            "price": "$1299"
        },
        {
            "id": "2",
            "category": "Smartphone",
            "brand": "Samsung",
            "model": "Galaxy S21",
            "screen": {
                "size": "6.2 inch"
            },
            "specs": {
                "RAM": "12GB",
                "processor": "Snapdragon 888",
                "storage": "128GB"
            },
            "price": "$999"
        },
        {
            "id": "3",
            "category": "Laptop",
            "brand": "Dell",
            "model": "XPS 13",
            "screen": {
                "size": "13.4 inch"
            },
            "specs": {
                "RAM": "16GB",
                "processor": "Intel Core i7",
                "storage": "512GB SSD"
            },
            "price": "$1499"
        },
        {
            "id": "4",
            "category": "Smartphone",
            "brand": "Apple",
            "model": "iPhone 13 Pro",
            "screen": {
                "size": "6.1 inch"
            },
            "specs": {
                "RAM": "6GB",
                "processor": "Apple A15 Bionic",
                "storage": "256GB"
            },
            "price": "$1099"
        },
        {
            "id": "5",
            "category": "Laptop",
            "brand": "HP",
            "model": "Envy x360",
            "screen": {
                "size": "13.3 inch"
            },
            "specs": {
                "RAM": "8GB",
                "processor": "AMD Ryzen 5",
                "storage": "256GB SSD"
            },
            "price": "$899"
        },
        {
            "id": "6",
            "category": "Smartphone",
            "brand": "Google",
            "model": "Pixel 6",
            "screen": {
                "size": "6.4 inch"
            },
            "specs": {
                "RAM": "8GB",
                "processor": "Google Tensor",
                "storage": "128GB"
            
            "price": "$799"
        },
        {
            "id": "7",
            "category": "Tablet",
            "brand": "Apple",
            "model": "iPad Air",
            "screen": {
                "size": "10.9 inch"
            },
            "specs": {
                "RAM": "4GB",
                "processor": "Apple A14 Bionic",
                "storage": "64GB"
            },
            "price": "$599"
        },
        {
            "id": "8",
            "category": "Tablet",
            "brand": "Samsung",
            "model": "Galaxy Tab S7",
            "screen": {
                "size": "11 inch"
            },
            "specs": {
                "RAM": "6GB",
                "processor": "Snapdragon 865+",
                "storage": "128GB"
            },
            "price": "$649"
        },
        {
            "id": "9",
            "category": "Laptop",
            "brand": "Lenovo",
            "model": "ThinkPad X1 Carbon",
            "screen": {
                "size": "14 inch"
            },
            "specs": {
                "RAM": "16GB",
                "processor": "Intel Core i5",
                "storage": "512GB SSD"
            },
            "price": "$1599"
        },
        {
            "id": "10",
            "category": "Smartphone",
            "brand": "OnePlus",
            "model": "9 Pro",
            "screen": {
                "size": "6.7 inch"
            },
            "specs": {
                "RAM": "12GB",
                "processor": "Snapdragon 888",
                "storage": "256GB"
            },
            "price": "$969"
        },
        {
            "id": "11",
            "category": "Laptop",
            "brand": "Microsoft",
            "model": "Surface Laptop 4",
            "screen": {
                "size": "13.5 inch"
            },
            "specs": {
                "RAM": "8GB",
                "processor": "Intel Core i5",
                "storage": "256GB SSD"
            },
            "price": "$1299"
        },
        {
            "id": "12",
            "category": "Smartphone",
            "brand": "Xiaomi",
            "model": "Mi 11",
            "screen": {
                "size": "6.81 inch"
            },
            "specs": {
                "RAM": "8GB",
                "processor": "Snapdragon 888",
                "storage": "128GB"
            },
            "price": "$749"
        },
        {
            "id": "13",
            "category": "Smartwatch",
            "brand": "Apple",
            "model": "Watch Series 7",
            "specs": {
                "RAM": "1GB",
                "processor": "Apple S7",
                "storage": "32GB"
            },
            "price": "$399"
        },
        {
            "id": "14",
            "category": "Camera",
            "brand": "Canon",
            "model": "EOS Rebel T7",
            "specs": {
                "sensor": "24.1MP APS-C CMOS",
                "lens": "EF-S 18-55mm f/3.5-5.6 IS II",
                "focus": "9-point AF"
            },
            "price": "$499"
        },
        {
            "id": "15",
            "category": "Headphones",
            "brand": "Sony",
            "model": "WH-1000XM4",
            "specs": {
                "type": "Over-ear",
                "noiseCancellation": "Active",
                "batteryLife": "Up to 30 hours"
            },
            "price": "$349"
        },
        {
            "id": "16",
            "category": "Gaming Console",
            "brand": "Sony",
            "model": "PlayStation 5",
            "specs": {
                "storage": "825GB SSD",
                "resolution": "Up to 8K"
            },
            "price": "$499"
        },
        {
            "id": "17",
            "category": "Smart Speaker",
            "brand": "Amazon",
            "model": "Echo Dot (4th Gen)",
            "specs": {
                "size": "Spherical",
                "voiceAssistant": "Alexa"
            },
            "price": "$49"
        },
    ]}

        # Initializes the handler
        prompt_handler = handler.prompt_handler
        
        # Collects the messages in a list of dicts
        messages = prompt_handler.get_messages(prompt_request)
         
        # For function calling functionality
        # functions = []
        # if prompt_request.function_call:
        #     functions = prompt_handler.get_functions()
        # print(functions)
 
        try:
            # Calls the main chat completion function
            prompt_response = await openai_service.chat_completion(
                messages=messages,
                CONFIG=CONFIG,
                functions=functions,
                client=client
            )
            print("prompt response")
            print(prompt_response)
            # Formats and returns
            response = prompt_handler.prepare_response(prompt_response)
            print("response")
            print(response)

        except Exception as e:
            traceback.print_exc()
            response = {"response": "Oops there was an error, please try again", "function_call": None}


        return {"response": ask_openai(user_message,data)}
    
    @router.post("/chat/function_call")
    async def function_call(function_call: FunctionCall):
        """Receives the function call from the frontend and executes it"""

        # debug
        print(function_call)

        # Preparing functions
        function_call_properties = jsonable_encoder(function_call)
        function_name = function_call_properties["name"]
        function_arguments = json.loads(function_call_properties["arguments"])
    
        # list of available functions
        available_functions = {
            # Obs: all functions need to be async
            "get_product_pages": lambda kwargs: functions.get_product_pages(CONFIG=CONFIG, **kwargs),
            "open_product_page": lambda kwargs: functions.open_product_page(CONFIG=CONFIG, **kwargs),
            "close_product_page": lambda _: functions.dummy_function(), # dummy function - no need of information
            "add_product_to_cart": lambda kwargs: functions.add_product_to_cart(CONFIG=CONFIG, **kwargs),
            "remove_product_from_cart": lambda kwargs: functions.remove_product_from_cart(CONFIG=CONFIG, **kwargs),
            "open_shopping_cart": lambda _: functions.dummy_function(), # dummy function - no need of information
            "close_shopping_cart": lambda _: functions.dummy_function(), # dummy function - no need of information
            "place_order": lambda _: functions.dummy_function(), # dummy function - no need of information
            "activate_handsfree": lambda _: functions.dummy_function(), # dummy function - no need of information
        }

        # Calling the function selected
        function_response = await available_functions[function_name](function_arguments)
        return {"response": function_response}

    @router.post("/chat/transcribe")
    async def generate_transcription(audio_req: AudioTranscriptRequest):
        """Receives the audio file from the frontend and transcribes it"""

        # Initializes the handler
        audio_handler = handler.audio_handler
        
        # Extracts the audio segment of the file
        audio_segment, _ = audio_handler.extract_audio_segment(audio_req.audio)

        # Send it as a tempfile path to openai - because that's the acceptable way to do it
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tmp_file:
            audio_segment.export(tmp_file.name, format="mp3")
            speech_filepath = Path(tmp_file.name)
            transcripted_response = await openai_service.whisper(audio_file=open(speech_filepath, "rb"), CONFIG=CONFIG, client=client)

        return {"response": transcripted_response}

    @router.post("/chat/tts")
    async def generate_tts(tts_req: AudioTTSRequest):
        """Receives the text from the frontend and generates the audio file"""

        # Generates the audio file
        audio = await openai_service.tts(text=tts_req.text, CONFIG=CONFIG, client=client)

        return {"response": audio}

    ## Retrieving from the database
    @router.get("/restaurants/")
    def get_restaurants(db: Session = Depends(get_db)):
        return db.query(Restaurant).all()
    
    @router.get("/restaurants/{restaurant_id}/foods/")
    def get_foods_from_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        foods = db.query(Foods).filter(Foods.restaurant_id == restaurant_id).all()
        return foods
    
    return router
    
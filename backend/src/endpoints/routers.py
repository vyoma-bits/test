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

def create_router(handler: MainHandler, CONFIG):
    router = APIRouter()
    client = handler.openai_client

    ## Question answering
    @router.post("/chat/send_message")
    async def send_message(prompt_request: ChatRequest):
        """Receives the chatlog from the user and answers"""

        # Initializes the handler
        prompt_handler = handler.prompt_handler
        
        # Collects the messages in a list of dicts
        messages = prompt_handler.get_messages(prompt_request)
        
        # For function calling functionality
        functions = []
        if prompt_request.function_call:
            functions = prompt_handler.get_functions()
        
        try:
            # Calls the main chat completion function
            prompt_response = await openai_service.chat_completion(
                messages=messages,
                CONFIG=CONFIG,
                functions=functions,
                client=client
            )
            
            # Formats and returns
            response = prompt_handler.prepare_response(prompt_response)

        except Exception as e:
            traceback.print_exc()
            response = {"response": "Oops there was an error, please try again", "function_call": None}


        return response
    
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
    
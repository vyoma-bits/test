from pydantic import BaseModel
from typing import Optional, List, Any, Dict

## OpenAI schema for Chat Completion
class FunctionCall(BaseModel):
    name: str
    arguments: str

class Message(BaseModel):
    content: str
    role: str
    function_call:FunctionCall
    
class Choices(BaseModel):
    finish_reason: str
    index: int
    message: Message

class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class OpenAIChatCompletionResponse(BaseModel):
    choices: Message
    created: int
    id: str
    model: str
    object: str
    usage: Usage

## Message System
class InputMessage(BaseModel):
    role: str
    content: Any
    name: Optional[str] = None

class InputChatHistory(BaseModel):
    history: List[InputMessage]

class ChatRequest(BaseModel):
    query: InputChatHistory
    


## Audio system
class AudioTranscriptRequest(BaseModel):
    audio: str
class AudioResponse(BaseModel):
    message: str

class AudioTTSRequest(BaseModel):
    text: str

from typing import List

class QueryMessage(BaseModel):
    id: str
    category: Optional[str] = None  # Make category optional with a default value or provide a valid value
    brand: Optional[str] = None
    model: Optional[str] = None  # Change to accept a single string value
    screen: Optional[str] = None
    specs: Optional[str] = None
    price: Optional[float] = None
    other_information: Optional[str] = None


    def __str__(self):
        return f"{{id: {self.id}, category: {self.category}, brand: {self.brand}, model: {self.model}, screen: {self.screen}, specs: {self.specs}, price: {self.price}, other_information: {self.other_information}}}"
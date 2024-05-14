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
    function_call: bool=True


## Audio system
class AudioTranscriptRequest(BaseModel):
    audio: str
class AudioResponse(BaseModel):
    message: str

class AudioTTSRequest(BaseModel):
    text: str

class QueryMessage(BaseModel):
    id: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    #screen parameter must be a dictionary with keys ram, processor, storage
    screen: Optional[Dict[str, str]] = None
    specs: Optional[Dict[str, str]] = None
    price: Optional[str] = None
    other_information: Optional[str] = None

    def __str__(self):
        return f"{{id: {self.id}, category: {self.category}, brand: {self.brand}, model: {self.model}, screen: {self.screen}, specs: {self.specs}, price: {self.price}, other_information: {self.other_information}}}"
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
storage = {}
class Message(BaseModel):
    sender: str
    receiver: str
    encrypted: str
    key: str
    nonce: str
    sender_lang: str
    receiver_lang: str
    emotion: str
    tagged_text: str
@app.post(&quot;/send&quot;)
def send_message(msg: Message):
    global storage
    storage = msg.dict()
    return {&quot;status&quot;: &quot;stored&quot;}
@app.get(&quot;/get&quot;)
def get_message():
    return storage

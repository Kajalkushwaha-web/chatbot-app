
from fastapi import FastAPI, Request


from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os


load_dotenv()

app=  FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)

@app.post("/chat")
async def chat(request:Request):
    data=await request.json()
    user_message=data.get("message","")
    
    if not user_message:
        return {"reply":"Please enter a message."}
    

    response=llm.invoke([HumanMessage(content=user_message)])
    return {"reply": response.content}






from fastapi import FastAPI, Request


from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from fastapi.responses import FileResponse
import os


load_dotenv()

app=  FastAPI()


@app.get("/")
async def read_index():
    return FileResponse('index.html')

# 2. Serve the CSS file
@app.get("/style.css")
async def read_css():
    return FileResponse("style.css")

# 3. Serve the JS file
@app.get("/script.js")
async def read_js():
    return FileResponse("script.js")




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

# @app.post("/chat")
# async def chat(request:Request):
#     data=await request.json()
#     user_message=data.get("message","")
    
#     if not user_message:
#         return {"reply":"Please enter a message."}
    

#     response=llm.invoke([HumanMessage(content=user_message)])
#     return {"reply": response.content}


@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        
        if not user_message:
            return {"reply": "Please enter a message."}
        
        # Check if API Key is actually loaded
        if not GEMINI_API_KEY:
             return {"reply": "Error: API Key is missing inside the container."}

        response = llm.invoke([HumanMessage(content=user_message)])
        return {"reply": response.content}
    except Exception as e:
        # This will tell us if it's an API error, a Network error, or a Code error
        return {"reply": f"Backend Error: {str(e)}"}





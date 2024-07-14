# from fastapi import FastAPI;
# from pydantic import BaseModel, HttpUrl;

# class VideoAnalysisRequest(BaseModel):
#     youtube_link: HttpUrl;
    
# app = FastAPI()

# @app.post("/analyze_video")
# def analyze_video(request: VideoAnalysisRequest):
#     return{
#         "youtube_link": request.youtube_link
#     }
# @app.get("/root")
# def health():
#     return {"status": "ok"}
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware

from services.genai import YoutubeProcessor, GeminiProcessor

class VideoAnalysisRequest(BaseModel):
    youtube_link: HttpUrl #advanced settings

app = FastAPI()
#configure CORS
app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials = True,
#     allow_methods=["*"],
#     allow_headers=["*"]
  CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust as needed for your frontend origin
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

genai_processor = GeminiProcessor(
    model_name = "gemini-1.5-flash",
    project="sample-dynamo"
)

@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisRequest):
   
    #Doing Analysis
    processor = YoutubeProcessor(genai_processor=genai_processor)
    result = processor.retrieve_youtube_documents(str(request.youtube_link), verbose=True) 
    
    #summary = genai_processor.generate_document_summary(result, verbose=True)   
    
    #Find Key concepts
    key_concepts = processor.find_key_concepts(result, sample_size=10, verbose=True )
    

    return{
      "key_concepts": key_concepts
    }
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel

app = FastAPI()

# Allow all origins for simplicity, but you can restrict this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_TOKEN = "71c6a876f9a6bcbe83b3a3f1a43466d83d3074d194064e9eb2fbc7dd2f6b5bac"
API_BASE_URL = "https://api.trytldw.ai/v1"

class MediaRequest(BaseModel):
    video_url: str

@app.post("/api/embed")
async def embed_video(media_request: MediaRequest):

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    
    media_list = [{
        "external_id": media_request.video_url,
        "title": media_request.video_url,
        "url": media_request.video_url
    }]

    try:
        response = requests.post(
            f"{API_BASE_URL}/media/embed",
            headers=headers,
            json={"media_list": media_list}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling tldw.ai API: {e}")

class StatusRequest(BaseModel):
    media_id: str

@app.get("/api/media/{media_id}")
async def get_media_status(media_id: str):

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
    }

    try:
        response = requests.get(
            f"{API_BASE_URL}/media/{media_id}?retrieve_description=true",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling tldw.ai API: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

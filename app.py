from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp
import uuid
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sab origins allow (testing ke liye)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.post("/download")
async def download_video(url: str = Form(...)):
    try:
        file_id = str(uuid.uuid4())
        out_file = os.path.join(DOWNLOADS_DIR, f"{file_id}.mp4")

        ydl_opts = {
            'format': 'best',
            'outtmpl': out_file
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return FileResponse(out_file, filename="video.mp4", media_type="video/mp4")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

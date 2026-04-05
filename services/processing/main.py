from fastapi import FastAPI, HTTPException
from tasks.pipeline import process_pipeline

app = FastAPI()

@app.post("/process")
def process(data: dict):
    try:
        job_id = data["job_id"]
        audio_path = data["audio_path"]

        process_pipeline(job_id, audio_path)

        return {
            "message": "Processing started",
            "job_id": job_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
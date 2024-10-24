from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RUN_URL = "http://127.0.0.1:8000"
UPLOAD_DIRECTORY = "storage"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@app.get("/files")
async def list_files():
    """Получить список всех загруженных файлов."""

    files = os.listdir(UPLOAD_DIRECTORY)
    return [
        {
            'filename': file.split("_")[1],
            'download': f"{RUN_URL}/files/{file.split("_")[0]}"
        }
        for file in files
    ]


@app.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Загрузить новый файл на сервер."""

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIRECTORY, file_id + "_" + file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_id": file_id, "filename": file.filename}


@app.get("/files/{fileId}")
async def download_file(fileId: str):
    """Скачать файл по идентификатору."""

    for filename in os.listdir(UPLOAD_DIRECTORY):
        if filename.startswith(fileId):
            file_path = os.path.join(UPLOAD_DIRECTORY, filename)
            return FileResponse(file_path, filename=filename.split("_", 1)[1])

    raise HTTPException(status_code=404, detail="Файл не найден")

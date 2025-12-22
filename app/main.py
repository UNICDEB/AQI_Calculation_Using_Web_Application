# import os, shutil, zipfile
# from fastapi import FastAPI, UploadFile, File, Request
# from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from processor import process_folder_in_memory

# app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# os.makedirs(UPLOAD_DIR, exist_ok=True)

# app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
# templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# TEMP_RESULT = {"file": None, "filename": None}

# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/process/")
# async def process(files: list[UploadFile] = File(...)):
#     shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
#     os.makedirs(UPLOAD_DIR)

#     for f in files:
#         path = os.path.join(UPLOAD_DIR, f.filename)
#         with open(path, "wb") as buffer:
#             shutil.copyfileobj(f.file, buffer)

#         if f.filename.endswith(".zip"):
#             with zipfile.ZipFile(path, 'r') as zip_ref:
#                 zip_ref.extractall(UPLOAD_DIR)

#     output, filename = process_folder_in_memory(UPLOAD_DIR)
#     TEMP_RESULT["file"] = output
#     TEMP_RESULT["filename"] = filename

#     return JSONResponse({"status": "success"})

# @app.get("/download/")
# def download():
#     if TEMP_RESULT["file"] is None:
#         return JSONResponse({"error": "No file processed"}, status_code=400)

#     return StreamingResponse(
#         TEMP_RESULT["file"],
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": f"attachment; filename={TEMP_RESULT['filename']}"}
#     )


import zipfile
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from processor import process_excel_streams
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

TEMP_RESULT = {"file": None, "filename": None}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process/")
async def process(files: list[UploadFile] = File(...)):
    excel_streams = {}

    for f in files:
        content = await f.read()

        # CASE 1: ZIP FILE
        if f.filename.lower().endswith(".zip"):
            with zipfile.ZipFile(BytesIO(content)) as z:
                for name in z.namelist():
                    if name.lower().endswith(".xlsx"):
                        excel_streams[os.path.basename(name)] = BytesIO(z.read(name))

        # CASE 2: DIRECT EXCEL
        elif f.filename.lower().endswith(".xlsx"):
            excel_streams[f.filename] = BytesIO(content)

    if not excel_streams:
        return JSONResponse({"status": "error", "message": "No Excel files found"}, status_code=400)

    output, filename = process_excel_streams(excel_streams)

    TEMP_RESULT["file"] = output
    TEMP_RESULT["filename"] = filename

    return {"status": "success"}


@app.get("/download/")
def download():
    if TEMP_RESULT["file"] is None:
        return JSONResponse({"error": "No processed file"}, status_code=400)

    return StreamingResponse(
        TEMP_RESULT["file"],
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={TEMP_RESULT['filename']}"
        }
    )

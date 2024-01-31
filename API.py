from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from search import clip_search
from fastapi.staticfiles import StaticFiles
import os, shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/similar_images", StaticFiles(directory="FoundImages"), name="similar_images")

def clear_folder(path):
    files = os.listdir(path)

    for file in files:
        file_path = os.path.join(path, file)
        os.remove(file_path)

@app.post("/upload")
async def load_image(file: UploadFile = File(...)):
    try:
         with open("uploaded_image.jpg", "wb") as f:
            f.write(file.file.read())
         return
    except HTTPException as e:
        return JSONResponse(content={"error": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/search")
async def get_search_results(query_path: str, dataset_path: str, device: str, n_results: int):
    try:
        search_results = clip_search(query_path, dataset_path, device=device, n_results=n_results)
        print(search_results)

        clear_folder(r"D:\TAREAS\App de busqueda\FoundImages")
        for file in search_results:
            source = os.path.join(r"D:\TAREAS\App de busqueda\test", file)
            destination = os.path.join(r"D:\TAREAS\App de busqueda\FoundImages" , file)
            shutil.copy(source, destination)

        return {"results": search_results}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during image search: {str(e)}",
        )

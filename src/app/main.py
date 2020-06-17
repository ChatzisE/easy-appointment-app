import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pkg_resources
from fastapi.responses import HTMLResponse,FileResponse
app = FastAPI()
app.mount("/static", StaticFiles(directory=pkg_resources.resource_filename(__name__, 'static')), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(pkg_resources.resource_filename(__name__, '/static/index.html'))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

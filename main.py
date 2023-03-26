#
import uvicorn
from fastapi import FastAPI

import setting
from rest.DemoRest import router

app = FastAPI(title=setting.title,
              description=setting.description,
              version=setting.version,
              docs_url="/demo/docs",
              redoc_url="/demo/redoc",
              openapi_url="/demo/openapi.json")

app.include_router(router, prefix="/demo")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

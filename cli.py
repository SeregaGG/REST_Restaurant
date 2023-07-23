import uvicorn
from src.settings import AppSettings


if __name__ == "__main__":
    app_settings = AppSettings()
    uvicorn.run("src.main:app", host=app_settings.HOST, port=app_settings.PORT)

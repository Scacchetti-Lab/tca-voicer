from fastapi import FastAPI
from app.constants.fastapi_doc import fastapi_data

app = FastAPI(
    title=fastapi_data["title"],
    summary=fastapi_data["summary"],
    description=fastapi_data["description"],
    contact=fastapi_data["contact"],
    version=fastapi_data["version"],
    license_info=fastapi_data["license"],
    redoc_url=None,
);

def main():
    print("Hello from tca-voicechat!")


if __name__ == "__main__":
    main()

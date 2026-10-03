from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    voicer_secret_key: str
    hf_token: str
    tts_host_url: str
    whisper_model: str
    callback_urls: str
    webhook_save_path: str
    vc_webhook_key: str

    model_config = SettingsConfigDict(env_file='.env')
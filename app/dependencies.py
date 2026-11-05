from functools import lru_cache
from faster_whisper import BatchedInferencePipeline, WhisperModel
from app.config import Settings

@lru_cache
def get_settings():
    return Settings() # type: ignore

@lru_cache(maxsize=1)
def get_whisper() -> BatchedInferencePipeline:
    env = get_settings()
    model = WhisperModel(env.whisper_model, device="cpu", compute_type="int8")
    return BatchedInferencePipeline(model=model)
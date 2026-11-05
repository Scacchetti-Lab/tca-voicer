from dataclasses import dataclass

# ===========================================================
# FROM tca-processing
# ===========================================================

@dataclass
class TitleGenerate:
    title: str

@dataclass
class InteractionId:
    interaction_id: str

@dataclass
class TextChunk:
    text: str

# ===========================================================
# FROM tca-voicer
# ===========================================================

@dataclass
class BotAudioChunk:
    bot_audio: str

@dataclass
class ErrorSSE:
    message: str
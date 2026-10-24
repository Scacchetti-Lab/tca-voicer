import re
from app.constants.constants import ALPHABET_LITERAL


_SIGLA = re.compile(r"(?<!\w)[A-Z]{2,}(?!\w)")
LIDAS_COMO_PALAVRA = {"TOTVS", "SAP", "OK", "PIX", "NASA"}


def _substring(m: re.Match) -> str:
    palavra = m.group(0)
    if palavra in LIDAS_COMO_PALAVRA:
        return palavra
    return " ".join(ALPHABET_LITERAL[c] for c in palavra)


def normalize_transcript(transcript: str) -> str:
    return _SIGLA.sub(_substring, transcript)
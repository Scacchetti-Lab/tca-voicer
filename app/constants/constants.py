from typing import Literal

DEFAULT_AUDIO_EXT= ["mp3", "m4a", "wav", "ogg", "opus", "aac", "flac", "webm"]
MP4_AUDIO_BRANDS = {b"M4A ", b"M4B ", b"isom", b"mp41", b"mp42", b"iso2", b"dash"}
SPEAKERS= Literal["ryan", "serena"]

ALPHABET_LITERAL = {
    "A": "á",     "B": "bê",    "C": "cê",    "D": "dê",
    "E": "é",     "F": "éfe",   "G": "gê",    "H": "agá",
    "I": "i",     "J": "jota",  "K": "cá",    "L": "éle",
    "M": "ême",   "N": "êne",   "O": "ó",     "P": "pê",
    "Q": "quê",   "R": "érre",  "S": "ésse",  "T": "tê",
    "U": "u",     "V": "vê",    "W": "dáblio","X": "xis",
    "Y": "ípsilon","Z": "zê",
}
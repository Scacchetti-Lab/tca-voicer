
__title = "TCA-VoicerAPI"
__description = """
## TCA-Voicer

Microserviço em Python focado em processamento de áudio, responsável por duas
funcionalidades específicas do sistema:

- Converter o áudio de transcrições de reunião em texto, integrando com o
  TCA-Processing para análise e persistência dos dados.
- Permitir conversa por voz com o TCA Chatbot, tirando dúvidas de forma
  rápida e mais imersiva do que digitando.

Requisições vindas através do backend principal (Java) chegam com a
identidade do usuário já resolvida via JWT, permitindo atribuir corretamente
quem realizou a transcrição ou quem está conversando com o chatbot.
Requisições vindas diretamente de dispositivos IoT, que não possuem
autenticação de usuário própria, são validadas apenas pela chave de acesso
compartilhada entre os serviços.

## Endpoints

### Voice

Endpoints principais responsáveis por transcrever o áudio de uma reunião ou
processar uma mensagem de voz enviada ao chatbot.

```
POST /voice/meeting (_not implemented_)
POST /voice/bot (_not implemented_)
```
"""
__summary = "Microserviço Python que transcreve áudio de reuniões e viabiliza conversa por voz com o chatbot do TCA."
__license = {
    "name": "License: PolyForm Noncommercial",
    "url": "https://github.com/Scacchetti-Lab/tca-voicer/blob/main/LICENSE",
    "identifier": "PolyForm-Noncommercial-1.0.0"
}
__version = "1.0.0"
__contact={
    "name": "Luís Scacchetti",
    "url": "https://github.com/scacchetti07",
}

fastapi_data = {
    "title": __title,
    "summary": __summary,
    "description": __description,
    "license": __license,
    "version": __version,
    "contact": __contact
}
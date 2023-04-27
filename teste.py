import pyttsx3

# Inicialize o objeto da engine de voz
engine = pyttsx3.init()

# Liste todas as vozes disponíveis
voices = engine.getProperty('voices')
for voice in voices:
    print("Nome: %s" % voice.name)
    print("Id: %s" % voice.id)
    print("Sexo: %s" % voice.gender)
    print("-----------------------------------------------------")

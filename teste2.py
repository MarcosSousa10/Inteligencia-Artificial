import pyttsx3

motor = pyttsx3.init()

vozes = motor.getProperty('voices')
voz_masculina = 2

motor.setProperty('voice', vozes[voz_masculina].id)
print(motor.setProperty('voice', vozes[voz_masculina].id)
)
motor.say('Olá, eu sou uma voz .')
print(motor.say('Olá, eu sou uma voz .')
)
motor.runAndWait()
print(motor.runAndWait()
)

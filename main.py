from models.medidor import Medidor
from controllers import socketController
from strategies import pressaoStrategy, temperaturaStrategy

try:
   
    controllerPressao1 = socketController.SocketTCPController(pressaoStrategy.PressaoStrategy(), 'pressao_events', 7555)
    controllerPressao2 = socketController.SocketTCPOnceController(pressaoStrategy.PressaoStrategy(), 'pressao_once_time', 7666)
    controllerTemperatura1 = socketController.SocketTCPController(temperaturaStrategy.TemperaturaStrategy(), 'temperatura_events', 8555)
    controllerTemperatura2 = socketController.SocketTCPOnceController(temperaturaStrategy.TemperaturaStrategy(), 'temperatura_once_time', 8666)

    medidor = Medidor()

    medidor.attach(controllerPressao1)
    medidor.attach(controllerPressao2)
    medidor.attach(controllerTemperatura1)
    medidor.attach(controllerPressao2)

    controllerPressao1.start()
    controllerPressao2.start()
    controllerTemperatura1.start()
    controllerTemperatura2.start()

    medidor.start()

    controllerPressao1.join()
    controllerTemperatura1.join()

        
except KeyboardInterrupt:
    print('process ended')

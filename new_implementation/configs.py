from . import AE_Peripheral, AE_Pin
config = [
    AE_Peripheral('Btn1', 'Stop knop', Switch(AE_Pin.D5)),
    AE_Peripheral('Btn2', 'Nog een knop', Switch(AE_Pin.D6)),
    AE_Peripheral('Btn3', 'Derde knop', Switch(AE_Pin.D6)),
    AE_Peripheral('Rly1', 'Fan 1 relais', Relay(AE_Pin(D16)))
]

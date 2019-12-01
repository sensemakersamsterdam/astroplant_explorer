from time import sleep
if True:
    import sys
    sys.path.append('..')
    from ae_drivers import AE_Pin
    from ae_drivers.button import AE_Button

btn1 = AE_Button('btn1', 'Just button 1', AE_Pin.D5)
btn1.setup()

btn2 = AE_Button('btn2', 'Just button 2', AE_Pin.D6)
btn2.setup()

btn3 = AE_Button('btn3', 'Just button 3', AE_Pin.D7, inverted=True)
btn3.setup()

print('Button demo.')
for n, b in enumerate([btn1, btn2, btn3]):
    print('btn%d prints as %s' % (n+1, str(b)))
    print('  and its description is:', b.description)

print('\nType Cntl-C to exit and press buttons 1-3 a few times...')

try:
    while True:
        print('\nSleeping 5 seconds.')
        sleep(5)
        print('  btn1.value()=', btn1.value())
        print('  btn1.pressed_count()=', btn1.pressed_count())
        print('  btn1.last_press_duration()=', btn1.last_press_duration())
except KeyboardInterrupt:
    print('\nBye bye...')

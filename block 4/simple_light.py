import time

def red(t):
    if 0<= t <360:
        return (0)
    elif 360<= t < 1320:
        return (0.2)
    else:
        return (0)

def blue(t):
    if 0<= t <360:
        return (0)
    elif 360<= t < 1320:
        return (0.1)
    else:
        return (0)
    
def farred(t):
    if 0<= t <360:
        return (0)
    elif 360<= t < 1320:
        return (0.05)
    else:
        return (0)

while True:
    thisminute= (time.localtime()[3] * 60 + time.localtime()[4])
    print("red is set to "+str(red(thisminute))+ ", blue to "+str(blue(thisminute))+ " and farred to "+str(farred(thisminute)))
    time.sleep(60)
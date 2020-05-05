import os
from time import sleep
from datetime import date, timedelta
from picamera import PiCamera
import ffmpeg
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT) #relay on pin 18

#camera params
camera = PiCamera()
delay = 900 #900 secs = 15 minutes
image_number = 0 #change starting number if necessary

if not os.path.isdir('./images'):
    os.mkdir('images') #make a new directory for todays images
    
#control params
last_check = date.today() #to decide whether make fresh folder and process images

#ffmpeg output options
output_options = {
    'pix_fmt': 'yuv420p'
}
    
while True:    
    #every day start with new folder    
    if not last_check == date.today():
        os.rename('images','processing')
        os.mkdir('images') #make a new directory for todays images
    #make picture
    GPIO.output(18, GPIO.HIGH) #switch light on
    sleep(2) #wait 2 seconds to stabilize light
    image_name = 'image{0:04d}.jpg'.format(image_number)
    camera.capture('images/' + image_name)
    image_number += 1
    GPIO.output(18, GPIO.LOW) #switch light off

    #process images of yesterday if neccessary
    if not last_check  == date.today():
        (
            ffmpeg
            .input('processing/*.jpg', pattern_type='glob', framerate=24) 
            .output(
                'out.mp4',
                **output_options
            )
            .run()
        )
        #archive processed images by day
        yesterday = str(date.today()- timedelta(days = 1))
        os.rename('processing','images'+ yesterday) 
        #if there is already a complete video of previous days cat the new to the existing
        if os.path.isfile('complete.mp4'):
            print('starting concat')
            ffmpeg.input('filelist.txt', format='concat', safe=0).output('new.mp4', c='copy').run()
            os.remove('complete.mp4')
            os.rename('new.mp4','complete.mp4')
        else:
            os.rename('out.mp4','complete.mp4') #for first time
        #change last_check to today
        last_check = date.today() 
        
    sleep(delay) # to be optimized because ffmpeg proccesing will delay too...

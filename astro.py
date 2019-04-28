import time
import datetime
import math
import os
import random
import logzero
import logging
from logzero import logger
from sense_hat import SenseHat
import ephem
anyException = False
# program Time is here for easy acces (in minutes)
programTime = 175
# 2:55 min of runtime

# ____________________________
#     DEFINE FUNCTIONS
# ____________________________

def setLoggingFile():
    '''
    This function will setup a logger and logfile
    '''
    # It will create a data01.csv file if it does not exist, data02.csv if previous exist etc
    # but when data01.csv data02.csv data03.csv data04.csv data05.csv exist it will overwrite the data01.csv file 

    try:
        # set dirPath
        dirPath = os.path.dirname(os.path.realpath(__file__))
        # set dir filenames 
        dirFiles = os.listdir(dirPath)
        for itemNr in range(len(dirFiles)):
            nameOfFile = 'data0'+str(itemNr+1)+".csv"
            if nameOfFile =='data05.csv':
                nameOfFile ='data01.csv'
                break
            if nameOfFile in dirFiles:
                print('this file exsist' + str(nameOfFile))
            else:
                break

    # Handle the Exception
    except Exception as dummy:
        # change global variable anyException to True, it will be logged at the end of run
        global anyException
        anyException = True 
        # set namefile to default one
        nameOfFile = 'data01.csv'
    # set logfile and custom formatter
    logzero.logfile(dirPath+"/"+nameOfFile)
    print(dirPath+"/"+nameOfFile)
    formatter = logging.Formatter('_%(levelname)s_,line: %(lineno)d, %(message)s')
    logzero.formatter(formatter)

def isItOversized():
    '''
    This function will check storage used to be sure files weight are less than 3gb
    '''
    try:
        # set dirPath
        dirPath = os.path.dirname(os.path.realpath(__file__))
        # set dir filenames 
        dirFiles = os.listdir(dirPath)
        # check files name
        filesSize = 0
        # add all files size to variable
        for file in dirFiles:
            filesSize+=os.stat(file).st_size
        # check that filesSize variable is less than 3221225472 bites which is 3gb
        # return False if it is smaller and return True when it is oversized
        if filesSize < 3221225472:
            return False
        else:
            return True
    # Handle the exception as default => not oversized 
    except Exception as e_oversizedFun_ecxeption:
        global anyException
        anyException = True 
        logger.error('Time from start: %s,Time is: %s,ERROR: %s',timer1.minsOfRun(),timer1.nowForLog(),str(e_oversizedFun_ecxeption))
        pictures('error')
        return False

def measure(whatToMeasure):
    '''
    This function will measure temperature, humidity and pressure
    '''

    # reset variables
    temp = 0
    hum = 0
    press = 0
    failed = 0
    
    try:
        # TEMPERATURE

        # Our code does 10 measurements
        # ignore the 0 - corrupted
        # and return the average result of measurements
        # if 5 measurements will be corrupted it will return an error

        if whatToMeasure == 'temp':
            print('TEMP MEASURE:')
            for dummy in range(10):
                # sleep betwen measurements
                time.sleep(0.2)
                while failed<5:
                    # get Temperature from SenseHat
                    tempNow=sh.get_temperature()
                    print(tempNow)
                    # if measured temp is okay break (while filed<5) loop
                    # always measured temp give us floats with decimals
                    # so if temp will be close to 0 measured temp will be for example 0.2312
                    # so if measured temp is equal to 0 without decimals measured temp is corrupted
                    if(tempNow != 0):
                        break
                    else:
                        # if cant get temperature (temp=0) add 1 to failed variable
                        failed+=1
                temp+=tempNow
            if(failed<5):
                # count the average data and round
                temp/=10
                temp=round(temp,2)
                print('MEASURED TEMP IS: '+str(temp))
            else:
                # error is returned as string becouse it will be displayed on screen (showInfo function)
                temp = 'ERROR'
            # return measured temp
            return temp

        # HUMidITY
        # same as temp but we measure humidity
        if whatToMeasure == 'hum':
            print('HUM MEASURE:')
            for dummy in range(10):
                time.sleep(0.2)
                while failed<5:
                    humNow=sh.get_humidity()
                    print(humNow)
                    if(humNow != 0):
                        break
                    else:
                        failed+=1
                hum+=humNow
            if(failed<5):
                hum/=10
                hum=round(hum,2)
                print('MEASURED HUM IS: '+str(hum))
            else:
                hum = 'ERROR'
            return hum
        # PRESSURE
        # same as temp but we measure pressure
        if whatToMeasure == 'press':
            print('PRESS MEASURE:')
            for dummy in range(10):
                time.sleep(0.2)
                while failed<5:
                    pressNow=sh.get_pressure()
                    print(pressNow)
                    if(pressNow != 0):
                        break
                    else:
                        failed+=1
                press+=pressNow
            if(failed<5):
                press/=10        
                press=round(press,2)
                print('MEASURED PRESS IS: '+str(press))
            else:
                press = 'ERROR'
            return press

    # handle exception and log it, display error image on screen
    except Exception as e_measure_eception:
        global anyException
        anyException = True
        logger.error('Time from start: %s,Time is: %s,ERROR: %s',timer1.minsOfRun(),timer1.nowForLog(),str(e_measure_eception))
        pictures('error')
        return "ERROR"

def pictures(idImg):
    '''
    This function displays images on SnenseHat pixel matrix scrren
    '''

    try:
        # Set display rotation on 0 deg
        rot = 0
        sh.set_rotation(rot)

        # Define some colors - keep brightness low 
        r = [50,0,0]
        g = [0,50,0]
        b = [0,0,50]
        p = [50,0,50]
        o = [0,0,0]
        w = [50,50,50]
        orientation = [0,90,180,270]
        # Define an images 
        
        welcome_img = [
        o,o,w,w,w,w,o,o,
        o,w,w,w,w,w,w,o,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        r,r,r,r,r,r,r,r,
        r,o,r,r,r,r,o,r,
        o,r,r,r,r,r,r,o,
        o,o,r,r,r,r,o,o,
        ]

        wait_img = [ 
        g,g,g,g,g,g,g,g, 
        o,g,o,o,o,o,g,o, 
        o,o,g,o,o,g,o,o, 
        o,o,o,g,g,o,o,o, 
        o,o,o,g,g,o,o,o, 
        o,o,g,g,g,g,o,o,
        o,g,g,g,g,g,g,o,
        g,g,g,g,g,g,g,g,
        ]

        temp_img1 = [
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,r,b,b,b,r,o,
        o,o,r,b,b,b,r,o,
        o,o,o,r,r,r,o,o,
        ]
        
        temp_img2 = [
        o,o,o,r,r,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,r,b,b,b,r,o,
        o,o,r,b,b,b,r,o,
        o,o,o,r,r,r,o,o,
        ]

        temp_img3 = [
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,r,b,b,b,r,o,
        o,o,r,b,b,b,r,o,
        o,o,o,r,r,r,o,o,
        ]

        temp_img4 = [
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,r,b,b,b,r,o,
        o,o,r,b,b,b,r,o,
        o,o,o,r,r,r,o,o,
        ]
        
        temp_img5 = [
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,b,r,o,o,
        o,o,r,b,b,b,r,o,
        o,o,r,b,b,b,r,o,
        o,o,o,r,r,r,o,o,
        ]

        temp_img6 = [
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,o,r,r,r,o,o,
        o,o,r,b,b,b,r,o,
        o,o,r,b,b,b,r,o,
        o,o,o,r,r,r,o,o,
        ]

        hum_img1 = [
        o,o,o,o,b,o,o,o,
        o,o,o,b,b,o,o,o,
        o,o,b,b,b,b,o,o,
        o,o,b,b,b,b,o,o,
        o,b,b,b,b,b,b,o,
        o,b,b,b,b,b,b,o,
        o,o,b,b,b,b,o,o,
        o,o,o,b,b,o,o,o,
        ]

        hum_img2 = [
        o,o,o,o,o,o,o,o,
        o,o,o,o,b,o,o,o,
        o,o,o,b,b,o,o,o,
        o,o,b,b,b,b,o,o,
        o,o,b,b,b,b,o,o,
        o,b,b,b,b,b,b,o,
        o,b,b,b,b,b,b,o,
        o,o,b,b,b,b,o,o,
        ]
        
        hum_img3 = [
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,b,o,o,o,
        o,o,o,b,b,o,o,o,
        o,o,b,b,b,b,o,o,
        o,o,b,b,b,b,o,o,
        o,b,b,b,b,b,b,o,
        b,b,b,b,b,b,b,b,
        ]
        
        hum_img4 = [
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,b,o,o,o,
        o,o,o,b,b,o,o,o,
        o,o,b,b,b,b,o,o,
        b,b,b,b,b,b,b,b,
        ]
        
        hum_img5 = [
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        ]

        press_img1 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        p,o,o,o,o,o,o,p,
        p,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img2 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        p,o,o,o,o,o,o,p,
        p,p,o,o,o,o,o,p,
        p,p,o,o,o,o,o,p,
        p,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img3 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,p,o,o,o,o,o,p,
        p,p,p,o,o,o,o,p,
        p,p,p,o,o,o,o,p,
        o,p,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img4 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,p,o,o,o,o,p,
        p,p,p,p,o,o,o,p,
        p,p,p,p,o,o,o,p,
        o,o,p,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img5 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,p,o,o,o,p,
        p,p,p,p,p,o,o,p,
        p,p,p,p,p,o,o,p,
        o,o,o,p,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img6 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,p,o,o,p,
        p,p,p,p,p,p,o,p,
        p,p,p,p,p,p,o,p,
        o,o,o,o,p,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img7 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,p,o,p,
        p,p,p,p,p,p,p,p,
        p,p,p,p,p,p,p,p,
        o,o,o,o,o,p,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img8 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,p,p,
        o,p,p,p,p,p,p,p,
        o,p,p,p,p,p,p,p,
        o,o,o,o,o,o,p,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img9 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,p,p,p,p,p,p,
        o,o,p,p,p,p,p,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img10 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,p,p,p,p,p,
        o,o,o,p,p,p,p,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img11 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,p,p,p,p,
        o,o,o,o,p,p,p,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img12 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,p,p,p,
        o,o,o,o,o,p,p,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img13 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,p,p,
        o,o,o,o,o,o,p,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]

        press_img14 = [
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        o,o,o,o,o,o,o,p,
        ]
        working_array= [
        g,g,g,g,g,g,g,g,
        g,g,g,g,g,g,g,g,
        g,g,g,g,g,g,g,g,
        g,g,g,g,g,g,g,g,
        g,g,g,g,g,g,g,g,
        g,g,g,g,g,g,g,g,
        g,g,g,g,g,g,g,g,
        g,g,g,g,g,g,g,g,
        ]
        error_array=[
        r,r,r,r,r,r,r,r,
        r,r,r,r,r,r,r,r,
        r,r,r,r,r,r,r,r,
        r,r,r,r,r,r,r,r,
        r,r,r,r,r,r,r,r,
        r,r,r,r,r,r,r,r,
        r,r,r,r,r,r,r,r,
        r,r,r,r,r,r,r,r,
        ]
        end_array=[
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        b,b,b,b,b,b,b,b,
        ]

        # routes to display diffrent images

        if idImg == 'welcome':
            sh.show_message('Welcome to PAPi', text_colour = w, scroll_speed=0.05)
            #This is a quote from one of a 'Country balls comics' 
            sh.show_message('Poland can ', text_colour = w, scroll_speed=0.05)
            sh.show_message('into space!', text_colour = r, scroll_speed=0.05)
            #Polish flag is upside down becouse this picture represent one of the 'Country balls'
            #specificaly a 'Poland ball', which have colors of Monako hahahaha!
            sh.set_rotation(180)
            sh.set_pixels(welcome_img)
            time.sleep(2)
            sh.set_rotation(0)
        # store multiple arrays (images) in one array for do an animation
        temp_array = [temp_img1, temp_img2,temp_img3, temp_img4, temp_img5, temp_img6, temp_img5, temp_img4, temp_img3, temp_img2, temp_img1]
        if idImg == 'temp':
            for temp_anim in temp_array:
                sh.set_pixels(temp_anim)
                time.sleep(0.1)
            
        hum_array = [hum_img1, hum_img2, hum_img3, hum_img4, hum_img5]
        if idImg == 'hum':
            for hum_anim in hum_array:
                sh.set_pixels(hum_anim)
                time.sleep(0.5)

        press_array = [press_img1, press_img2, press_img3, press_img4, press_img5,press_img6, press_img7, press_img8, press_img9, press_img10, press_img11, press_img12, press_img13, press_img14]
        if idImg == 'press':
            for press_anim in press_array:
                sh.set_pixels(press_anim)
                time.sleep(0.1)

        if idImg == 'end':
            sh.set_pixels(end_array)
            time.sleep(0.3)

        if idImg == 'error':
            sh.set_pixels(error_array)
            time.sleep(0.5)
        if idImg == 'wait':
            sh.set_pixels(wait_img)
            # here we have animation by rotate the screen
            for rot in orientation:
                sh.set_rotation(rot)
                time.sleep(0.2)

        # if given parameter was not equal to wait and or error show us a greeen image until next function call
        # green image means that everything is okay
        if (idImg != 'wait' and idImg != 'end' and idImg != 'error'):
            sh.set_pixels(working_array)

    # Handle the exception
    except Exception as e_display_eception:
        global anyException
        anyException = True 
        logger.error('Time from start: %s,Time is: %s,ERROR: %s',timer1.minsOfRun(),timer1.nowForLog(),str(e_display_eception))
        return "ERROR"

def showInfo(measure):
    '''
    that function gets random color and displays measure parameter on SenseHat screen
    '''
    try:
        # define RGB colors
        r = [50,0,0]
        g = [0,50,0]
        b = [0,0,50]
        p = [50,0,50]
        c = [0,50,50]
        u = [50,50,0]
        # store all colors in one array for easier draw
        textColours = [r,g,b,p,c,u]
        # get random color
        color = textColours[random.randint(0,len(textColours)-1)]
        # set rotation to 0 degrees
        sh.set_rotation(0)
        # show message
        sh.show_message(str(measure), text_colour =color, scroll_speed=0.05)
        # sleep one secound
        time.sleep(1)

    # handle the exception
    except Exception as e_displayText_exception:
        logger.error('cannot show message on senseHat: %s',e_displayText_exception)
        pictures('error')
def ephemISS():
    '''
    Ephem module funciton
    '''
    try:
        # ehem computing for logs
        # SOURCE = CELESTREAK.COM 
        # DAY = 26.01.2019
        nameOfStation = 'ISS (ZARYA)'
        firstLine = '1 25544U 98067A   19027.58387731  .00001656  00000-0  33287-4 0  9996'
        secondLine = '2 25544  51.6426 340.5081 0004927 322.6857  20.8029 15.53199695153409'
        stationISS = ephem.readtle(nameOfStation,firstLine,secondLine)
        stationISS.compute()

        # calculate result
        if(stationISS.sublat)<0:
            return 'ISS is in Southern hemisphere'
        else:
            return 'ISS is in Northern hemisphere'
    # handle the exception
    except Exception as e_ISS_eception:
        global anyException
        anyException = True 
        logger.error('Cannot get EPHEM resulit eroor:%s',str(e_ISS_eception))
        pictures('error')
        return "ERROR"


class timer:
    '''
    Timer obiect give us easier ability to count time and get better logs

    '''

    # set start time and end time of obiect
    def __init__(self):
        # get start time from datatime module
        self.startTime = datetime.datetime.now()
        # count the endtime, programTime was defined at the top
        self.endTime = self.startTime + datetime.timedelta(minutes=programTime)

    def minsOfRun(self):
        # cuted output for logs
        # example '0:00:27' - how much time program is already running
        return str(datetime.datetime.now()-self.startTime)[:7] 
    def now(self):
        # return datetime obiect for check actual time
        self.time = datetime.datetime.now()
        return self.time
    def nowForLog(self):
        # cuted output for nicer logs:
        # example '14:52:32'
        return str(datetime.datetime.now())[11:19]

# ____________________________
#     INICIALIZE PROGRAM
# ____________________________

try:
    # set timer obiect
    timer1 = timer()
    # call function to setup logging
    setLoggingFile()
    # first log
    logger.debug('starting program,time is: %s, program will be running for: %smin',timer1.now(),programTime)
    # log ephem return
    logger.info('EPHEM: %s',ephemISS())
    # connect to SenseHat
    sh = SenseHat()
    # sleep 2 sec
    time.sleep(2)
    # show welcome screen
    pictures('welcome')# 

# handle the exception
except Exception as e_init_exception:
    anyException = True 
    logger.error('INIT ERROR: %s',str(e_init_exception))

# ____________________________
# SET VARIABLES
# ____________________________

averageTemp=0
averageHum=0
averagePress=0
rounds = 0
lowestTemp = 9999999999
lowestHum = 9999999999
lowestPress = 9999999999
higestTemp = 0
higestHum = 0
higestPress = 0

# ____________________________
# MAIN LOOP OF PROGRAM
# ____________________________

# while timer1 obiect (time now) is smaller than (endTime)
while(timer1.now()<timer1.endTime):
    try:
        # check oversize function return
        if(isItOversized()):
            logger.debug('OVERSIZED EXITING')
            break


        # add rounds (average measurements will be calculate on this variable)
        rounds+=1
        # log round and time for start
        logger.debug('Start round: %s,Time from start: %s',rounds,timer1.minsOfRun())
        # show wait image and show active round on screen
        pictures('wait')
        showInfo('round: '+str(rounds))

        # show temperature animation, measure temperature and display result on screen 
        pictures('temp')
        tempNowIs = measure('temp')
        showInfo(str(tempNowIs)+" 'C")

        # same to humidity
        pictures('hum')
        humNowIs = measure('hum')
        showInfo(str(humNowIs)+' %')

        # same to pressure
        pictures('press')
        pressNowIs = measure('press')
        showInfo(str(pressNowIs)+' mbar')

        # log all results
        logger.info('Time is: %s,Time from start: %s,Temp: %s,Hum: %s,Press: %s',timer1.nowForLog(),timer1.minsOfRun(),tempNowIs,humNowIs,pressNowIs)


        # if there was not any error count lower, higest and average measurements
        if(tempNowIs != 'ERROR' and humNowIs != 'ERROR' and pressNowIs != 'ERROR'):
            averageTemp+=tempNowIs
            averageHum+=humNowIs
            averagePress+=pressNowIs

            if tempNowIs<lowestTemp:
                lowestTemp = tempNowIs
            if tempNowIs>higestTemp:
                higestTemp = tempNowIs

            if humNowIs < lowestHum:
                lowestHum = humNowIs
            if humNowIs>higestHum:
                higestHum = humNowIs

            if pressNowIs<lowestPress:
                lowestPress = pressNowIs
            if pressNowIs>higestPress:
                higestPress = pressNowIs
        else:
            # if there was an error dont count this round
            rounds-=1

    # handle main exception
    except Exception as e_main_exception:
        anyException = True 
        logger.error('Time from start: %s,Time is: %s,ERROR: %s',timer1.minsOfRun(),timer1.nowForLog(),str(e_main_exception))
        pictures('error')


# ____________________________
#     AFTER MAIN LOOP
# ____________________________


try:
    # calculate and round average measurements
    averageTemp/=rounds
    averageHum/=rounds
    averagePress/=rounds
    averageTemp = round(averageTemp,2)
    averageHum = round(averageHum,2)
    averagePress = round(averagePress,2)
    lowestTemp = round(lowestTemp,2)
    lowestHum = round(lowestHum,2)
    lowestPress = round(lowestPress,2)
    higestTemp = round(higestTemp,2)
    higestHum = round(higestHum,2)
    higestPress = round(higestPress,2)

    # log all
    logger.info('average Temp: %s,average hum: %s,average press: %s',averageTemp,averageHum,averagePress)
    logger.info('Temp: highest: %s lowest: %s ,Hum: highest: %s lowest: %s ,Press: highest: %s lowest: %s',higestTemp,lowestTemp,higestHum,lowestHum,higestPress,lowestPress)
    logger.debug('code succesfully exited after: %s,expected time: %smin, time of end is: %s, problems: %s',timer1.minsOfRun(),programTime,timer1.now(),anyException)
    logger.debug('program ended with %s rounds of collecting data',rounds)
    # say goodbye
    pictures('end')
# exit on that Exception
except Exception as e_sumUp_exception:
    print('CANNOT SUMUP DATA, EXITING')
    logger.error('SUMUP ERROR: %s',str(e_sumUp_exception))
    exit()
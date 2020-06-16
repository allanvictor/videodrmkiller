from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import os
from subprocess import Popen, PIPE
import signal
from xvfbwrapper import Xvfb

class Bot():
    def __init__(self):
        self.virtualdisplay = Xvfb(width=1920, height=1080, display=1)
        self.virtualdisplay.start()
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
        self.browser = webdriver.Chrome(options=self.chrome_options)
    def enterSite(self, site):
        self.browser.get(site)
    def waitElementLoad(self,elementxpath):
        self.delay = 3
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, elementxpath)))
        except TimeoutException:
            print('Loading took too much time!')
    def clickButton(self, elementxpath):
        self.browser.find_element_by_xpath(elementxpath).click()
    def startRecordVideo(self, outputvideo):
        print ('--start recording--')
        self.record_proccess = Popen('/usr/bin/ffmpeg -y -f x11grab -video_size 1920x1080  -probesize 48M -i :1 -f pulse -ac 2 -i default -c:v libx264 -preset superfast -crf 18 -pix_fmt yuv420p '+outputvideo, shell=True)
    def calculateVideotime(self, videotime):
        self.videotime = self.browser.find_element_by_xpath(videotime)
        self.videotime = self.videotime.get_attribute('innerHTML')
        self.videotime = datetime.strptime(self.videotime,'%M:%S')
        return self.videotime.second + self.videotime.minute*60 + self.videotime.hour*3600
    def finishing(self):
        print ('--stop recording--')
        os.kill(self.record_proccess.pid, signal.SIGINT)
        self.virtualdisplay.stop()

if __name__ == '__main__':
    bot = Bot()
    bot.enterSite('https://site.teste.com.br')
    elements = []
    # play button
    playvideobutton = '/html/body/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[3]/div/button/div'
    # unmute video
    audiobutton = '/html/body/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[5]/div/div[3]/div/button[2]'
    # fullscreen button
    fullscreenbutton = '/html/body/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[5]/div/div[3]/div/button[8]'
    videotime = '/html/body/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[5]/div/div[2]/div/span[2]'
    elements.append(playvideobutton)
    elements.append(audiobutton)
    elements.append(fullscreenbutton)
    bot.waitElementLoad(elements[0])
    for button in elements:
        bot.clickButton(button)
    bot.startRecordVideo('video3.mkv')
    time.sleep(bot.calculateVideotime(videotime))
    bot.finishing()
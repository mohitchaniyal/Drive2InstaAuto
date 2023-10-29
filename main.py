from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import json
from datetime import datetime
import requests
import os
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1920, 1200))  
display.start()


class Drive2InstaAuto:
    def __init__(self):
        self.__day = os.getenv('DAY')
        self.__file_id=os.getenv('FILE_ID')
        self.__TAGS=os.getenv('TAG')
        self.__browser=None
        self.__JS_DROP_FILE = """
            var target=arguments[0],offsetX=arguments[1],offsetY=arguments[2],document=target.ownerDocument||document,window=document.defaultView||window;
            var input=document.createElement('INPUT');input.type='file';input.onchange=function(){var rect=target.getBoundingClientRect(),x=rect.left+(offsetX||(rect.width>>1)),y=rect.top+(offsetY||(rect.height>>1)),dataTransfer={files:this.files};
            ['dragenter','dragover','drop'].forEach(function(name){var evt=document.createEvent('MouseEvent');evt.initMouseEvent(name,!0,!0,window,0,0,0,x,y,!1,!1,!1,!1,0,null);
            evt.dataTransfer=dataTransfer;target.dispatchEvent(evt);});setTimeout(function(){document.body.removeChild(input);},25);};
            document.body.appendChild(input);return input;
        """
        self.__file_path=os.getenv('GITHUB_WORKSPACE')+"/doggo.mp4"
        self.__day=datetime.today().date()-datetime.strptime(self.__day,"%d-%m-%Y").date()
        
    def __get_file(self):
        try:
            URL = f"https://drive.google.com/uc?id={self.__file_id}"
            response=requests.get(URL,stream=True)
            with open("doggo.mp4","wb") as f:
                f.write(response.content)
        except Exception as e:
            print(e)

    def __initialize_browser(self):
        try:
            url='https://www.instagram.com/'
            driver_path = 'chromedriver-linux64/chromedriver'
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            browser = Chrome(service=Service(driver_path),options=chrome_options)
            browser.implicitly_wait(5)
            browser.get(url)
            browser.maximize_window()
            self.__browser=browser
            return {"success":True}
        except Exception as e:
            print(e)
    
    def __login(self):
        try:
            with open("insta.json", 'r') as cookiesfile:
                cookies = json.load(cookiesfile)
            for cookie in cookies:
                self.__browser.add_cookie(cookie)
            self.__browser.get("https://www.instagram.com/")
            time.sleep(2)
            # self.__browser.find_element(By.XPATH,"//button[text()='Not Now']").click()
            return {"success":True}
        except Exception as e:
            self.__browser.save_screenshot("screenshot.png")
            print(e)
    
    def __upload_post(self):
        try:
            self.__browser.find_element(By.XPATH,"//span[text()='Create']").click()
            time.sleep(1)
            element=self.__browser.find_element(By.XPATH,"//span[text()='Create']")
            driver = element.parent
            file_input = driver.execute_script(self.__JS_DROP_FILE,element, 0, 0)
            time.sleep(2)
            file_input.send_keys(self.__file_path)
            time.sleep(2)
            self.__browser.find_element(By.XPATH,"//button[text()='OK']").click()
            self.__browser.find_element(By.XPATH,"//div[text()='Next']").click()
            self.__browser.find_element(By.XPATH,"//div[text()='Next']").click()
            self.__browser.find_element(By.XPATH,"//div[text()='Write a caption...']/..//p").send_keys(f"Day {self.__day} \n He will stop crying after 1M followers \n {self.__TAGS} ")
            self.__browser.find_element(By.XPATH,"//div[text()='Share']").click()
            time.sleep(20)
            self.__browser.save_screenshot("screenshot.png")
            return {"success":True}
        except Exception as e:
            self.__browser.save_screenshot("screenshot.png")
            print(e)
        
    
    def _start_uploding_file(self):
        self.__initialize_browser()
        self.__login()
        self.__get_file()
        self.__upload_post()
        time.sleep(5)
        self.__browser.close()
        return {"success":True}
    
    @classmethod
    def pipeline_handler(cls):
        cls()._start_uploding_file()
        return {"success":True}
        
if __name__=="__main__": 
    Drive2InstaAuto.pipeline_handler()
    

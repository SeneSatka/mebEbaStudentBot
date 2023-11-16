from selenium.webdriver import Firefox,FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
class types:
    class go:
      class menu:
        sayfam=0
        ebaPortfolyo=1
        dersler=2
        canliDersler=3
        sinavlar=4
        kutuphane=5
        digitalCalismalarim=7
        sozluVeYaziliCalismalarim=8
        dosyalar=9
        takvim=10
        gruplar=11
        ebaAnaSayfayaDon=12
      class ebaPortfolyo:
        hakkinda=100
        ebaPuaniVeSiralamasi=101
        armalar=102

      @staticmethod 
      def dersler(ders:str):
         return ders.replace("İ","i").replace("I","ı").lower()
         
    
class student:
    tckn=""
    passwd=""
    options=FirefoxOptions()
    browser=None
    def __init__(self,tckn,passwd,show:str=False):
        if show==False:
         self.options.add_argument("--headless")
        self.browser=Firefox(options=self.options)
        self.browser.set_window_position(0,0)
        self.wait = WebDriverWait(self.browser, 10)
        self.tckn=tckn
        self.passwd=passwd

    def login(self):
        self.browser.get("https://giris.eba.gov.tr/EBA_GIRIS/student.jsp")
        tckn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tckn"]')))
        passwd = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
        login = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="studentUst"]/div/form/div[2]/button')))
        tckn.send_keys(self.tckn)
        passwd.send_keys(self.passwd)
        login.click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vc-feedList"]')))
        print(f"Login succefully!\nTckn: {self.tckn[:3]}********\nPasswd: **********")

    def go(self,to):
        menuitems= self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="vc-left-menu-item"]')))
        if type(to) is int:
            if to <= 12 and to >= 0:
                menuitems[to].click()
                self.wait.until(EC.visibility_of_element_located,(By.XPATH,'//*[@id="dashboardProfileScorePage"]/div[2]/div/div'))
            elif to <= 200 and to >=100:
                menuitems[types.go.menu.ebaPortfolyo].click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="portfolioDashboardHeader"]/div/div[2]/div[1]/div[2]/div'))).click()
                item=self.wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="target{str(to)[2]}"]')))
                item.click()
        elif type(to) is str:
           menuitems[types.go.menu.dersler].click()
           dersler = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="vcLessonPage"]')))
           time.sleep(1)
           for i in range(len(dersler.find_elements(By.XPATH,"./div/div")[0].find_elements(By.XPATH,"./div"))):
            ders = self.browser.find_elements(By.CSS_SELECTOR,f"#vcLessonPage > div.hidden-sm.hidden-md.hidden-lg.m-t-md.m-r-md.m-l-md.ng-scope > div:nth-child({i + 1}) > div > div.vc-display-inline-block.vc-position-absolute.vc-inheritHeight > div > span")
            time.sleep(1)
            if len(ders)>0:
             if types.go.dersler(self.browser.execute_script("return arguments[0].innerText;", ders[0]))==to:
                self.browser.execute_script("arguments[0].click();", self.browser.find_element(By.XPATH, f'  //*[@id="vcLessonPage"]/div[1]/div/div[{i+1}]/div/div/div[1]'))
                break
          
              

    def screenshot(self,path):
        time.sleep(2)
        self.browser.save_screenshot(path)
    def __del__(self):
        time.sleep(10)        
        self.browser.close()
        self.browser.quit()   




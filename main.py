#coding=utf-8
import logging
import os
from random import random
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass


def main():
    netid = os.getenv("netid")
    password = os.getenv("password")
    options = webdriver.ChromeOptions()

    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    with open('./stealth.min.js') as f:
        js = f.read()
    
    #options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

    driver.get("http://jkrb.xjtu.edu.cn/EIP/user/index.htm")

    wait = WebDriverWait(driver=driver, timeout=30)
    wait.until((EC.url_contains("org.xjtu.edu.cn")))
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/input[1]'))
    )
    elem.send_keys(netid)
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/input[2]'))
    )
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)

    try:
        wait.until(EC.url_contains("http://jkrb.xjtu.edu.cn/EIP/user/index.htm"))
    except Exception:
        logger.info("nothing")
    logger.info("Successful Login")

    
    wait_for_ajax(driver)
    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload2()']")
    driver.switch_to.frame(iframe)

    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload1()']")
    driver.switch_to.frame(iframe)


    iframe=driver.find_element_by_xpath('//div[@title="研究生每日健康状况填报"]') 
    
    iframe.click()
    driver.implicitly_wait(1)
    driver.switch_to.default_content()
    driver.implicitly_wait(5)
    
    iframe = driver.find_element_by_xpath(
        "//iframe[@onload='__iframe_onload3()']")
    driver.switch_to.frame(iframe)
    iframe= driver.find_element_by_xpath(r'//li[@data-blname="每日健康填报"]')
    iframe.click()
    driver.implicitly_wait(1)
    driver.switch_to.default_content()
    driver.implicitly_wait(5)

    try :
        iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload4()']")
        driver.switch_to.frame(iframe)
        iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload1()']")
        driver.switch_to.frame(iframe)
        temp = str(round(36 + random(), 1))
        driver.find_element_by_xpath(
            '//*[@id="BRTW$text"]'
        ).send_keys(temp)
        
        print('st 确认须知')
        driver.find_element_by_xpath('//*[@id="mini-2$ck$0"and @value="1"]').click()
        #确认须知
        #driver.find_element_by_xpath('//input[@id="mini-11$ck$1" ]').click()
        
        #日期
        
        
        date = time.localtime(time.time()-8*3600)

        send_date = str(date.tm_year)+'-'+str(date.tm_mon)+'-'+str(date.tm_mday)+" 18:31"

        
        data_input = driver.find_element_by_xpath('//*[@id="ZJYCHSJCSJ$text"]')
        time.sleep(5)
        data_input.clear()
        data_input.send_keys(send_date)

        
        driver.find_element_by_xpath('//*[@id="mini-5$ck$0" and @value="是"]').click()
        driver.find_element_by_xpath('//*[@id="mini-10$ck$1" and @value="阴性"]').click()
        driver.find_element_by_xpath('//*[@id="mini-11$ck$0" and @value="未被隔离"]').click()
        driver.find_element_by_xpath('//*[@id="mini-12$ck$2" and @value="绿色"]').click()
        

        logger.info(f"Today's body temp. is {temp}")
        driver.switch_to.default_content()
        driver.implicitly_wait(5)
        iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload4()']")
        driver.implicitly_wait(5)
        driver.switch_to.frame(iframe)
        submit=driver.find_element_by_xpath('//*[@id="sendBtn"]')
        submit.click()

        driver.implicitly_wait(5)
        submit=driver.find_element_by_xpath('//*[@id="mini-17"]/span')
        submit.click()
        try:
            driver.switch_to.default_content()
            driver.implicitly_wait(1)
            iframe = driver.find_element_by_xpath(
                "//iframe[@onload='__iframe_onload4()']"
            )
            driver.switch_to.frame(iframe)
            elem = driver.find_element_by_xpath("//*[@id='mini-19$content']")
            logger.info(elem.text)
        except NoSuchElementException:
            logger.info("Successful submit!")
    except NoSuchElementException:
        driver.switch_to.default_content()
        iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload5()']")
        driver.switch_to.frame(iframe)
        elem = driver.find_element_by_xpath("//*[@id='messageId']")
        logger.info("You've already checked in.")
        logger.info(elem.text)








if __name__ == "__main__":
    main()
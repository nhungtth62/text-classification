from selenium import webdriver
from time import sleep
import chromedriver_binary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import codecs
import csv


def load_url_selenium_tiki(url, rating):
    
    chrome_options = Options()
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_argument("--headless") 
    # chrome_options.add_argument("--kiosk") ---- fullscreen
    chrome_options.add_argument("--start-maximized") #---- max windown
    driver = webdriver.Chrome(executable_path='C:/Users/nhung/Desktop/CommentClassification/chromedriver.exe', chrome_options= chrome_options)
 
    # driver = webdriver.Chrome(executable_path='C:/Users/nhung/Desktop/CommentClassification/chromedriver.exe')
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>Loading url=", url, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    driver.get(url)
    list_review = []
  
    driver.refresh()
    wait = WebDriverWait(driver, 30)
    sleep(2)
    driver.execute_script("window.scrollTo(0, 2000);")
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.customer-reviews__inner")))

    filter_button = driver.find_elements_by_xpath("//*[@data-view-index= '" + str(8- rating)  + "'][@data-view-id ='pdp_review_filter_item' ]")
    filter_button[0].click()
    
    driver.execute_script("window.scrollTo(0, 2500);")
    x = 0
    while x < 15 : 
        sleep(5)
        
        product_reviews = driver.find_elements_by_xpath("//*[@class='style__StyledComment-sc-103p4dk-5 hMjYZK review-comment']")
        
        for review_info in product_reviews:
            review = review_info.find_element_by_css_selector("[class='review-comment__content']").text
            
            if (review != "" or review.strip()):
                print(review, "\n")
                list_review.append(review)   
         
        button_next = driver.find_elements_by_css_selector("[class='btn next']")
        if len(button_next) == 0:
            break
        else:
            element = driver.find_element_by_class_name('next')
            # driver.execute_script("arguments[0].click();", element)
            sleep(5)
            button_next[0].click()
            x = x + 1

    driver.close()
    print("-----------Có " , len(list_review), " bình luận về sản phẩm ", rating, "-------------------")
    with open(r'C:/Users/nhung/Desktop/CommentClassification/data_collection.csv', "a", encoding= 'utf-8', newline='\n') as f:
        writer = csv.writer(f)
        for review in list_review:
            writer.writerow([review, str(rating)])

def load_url_selenium_shopee(url, rating):
    try: 
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized") #---- max windown
        chrome_options.add_argument("--headless") 
        driver = webdriver.Chrome(executable_path='C:/Users/nhung/Desktop/CommentClassification/chromedriver.exe', chrome_options= chrome_options)

        # driver = webdriver.Chrome(executable_path='C:/Users/nhung/Desktop/CommentClassification/chromedriver.exe')
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>Loading url=", url, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        driver.get(url)
        list_review = []
    
        driver.refresh()
        wait = WebDriverWait(driver, 30)
        sleep(3)
        driver.execute_script("window.scrollTo(0, 1800);")
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div._3-GQHh")))
        sleep(5)
        filter_button = driver.find_elements_by_xpath("//*[@class = 'product-rating-overview__filter']")

        if len(filter_button) == 0:
            driver.execute_script("window.scrollTo(0, 2800);")
            sleep(5)
            filter_button = driver.find_elements_by_xpath("//*[@class = 'product-rating-overview__filter']")

        filter_button[5-rating].click()
        driver.execute_script("window.scrollTo(0, 2500);")
        x = 0

        while x < 15 : 
            sleep(3)
            isLoop = True

            product_reviews = driver.find_elements_by_xpath("//*[@class='shopee-product-rating']")

            if len(product_reviews) < 6:
                isLoop = False

            for review_info in product_reviews:
                review = review_info.find_element_by_css_selector("[class='shopee-product-rating__content']").text
                
                if (review != "" and review.strip() != "" ):
                    if len(list_review) - 6 >= 0 and len(list_review) % 6 == 0:
                        if review != list_review[len(list_review) - 6] : 
                            print(review, "\n")
                            list_review.append(review)   
                            print("----------------------")
                        else:
                            isLoop = False
                            break
                    else:
                        print(review, "\n")
                        list_review.append(review)   
                        print("----------------------")
                    
                else:
                    isLoop = False
                    break
           
            if isLoop :
                button_next = driver.find_elements_by_css_selector("[class='shopee-icon-button shopee-icon-button--right ']")
            #  driver.execute_script("arguments[0].click();", button_next)    
                button_next[0].click()       
                x = x + 1   
                count_pre_loop = len(list_review)
            else:
                break

    except Exception as e: 
        print(e)
        print("============> error: " + url)

    finally:
        driver.close()
 
    print("-----------Có " , len(list_review), " bình luận về sản phẩm --", rating, "-----------------")
    with open(r'C:/Users/nhung/Desktop/CommentClassification/data_collection.csv', "a", encoding= 'utf-8', newline='\n') as f:
        writer = csv.writer(f)
        for review in list_review:
            writer.writerow([review, str(rating)])

def saveDataTiki(url):
    # for rating in [3,4,5,6,7]:
    for rating in [1,2,3,4,5]:
        load_url_selenium_tiki(url, rating)

def saveDataShoppe(url):
    for rating in [1,2,3,4]:
        load_url_selenium_shopee(url, rating)    


tiki_urls = [
   
]


shoppe_urls = [
#     "https://shopee.vn/S%C3%A9t-b%E1%BB%99-h%C3%A8-b%C3%A9-g%C3%A1i-szie-4-20kg-i.139249395.2101323588",
#     "https://shopee.vn/B%E1%BB%99-b%C3%A9-g%C3%A1i-(-2-tim-3rua-)-size-7-19kg-i.139249395.2116642122",
#     "https://shopee.vn/B%E1%BB%99-Ch%C3%A0ng-Trai-%C4%90eo-K%C3%ADnh-Ch%E1%BA%A5t-Li%E1%BB%87u-Cotton-X%C6%B0%E1%BB%9Fng-May-DCS-i.277394200.9742619832",
#    "https://shopee.vn/%C3%81o-thun-NELLY-tay-l%E1%BB%A1-tr%C6%A1n-i.111783192.5760439879",
#    "https://shopee.vn/%C3%81o-thun-nam-n%E1%BB%AF-unisex-tay-l%E1%BB%A1-LF-84-%C3%A1o-ph%C3%B4ng-tay-l%E1%BB%A1-unisex-form-r%E1%BB%99ng-oversize-streetwear-i.385915342.3030423818",
#    "https://shopee.vn/-M%C3%A3-WAMT1505-gi%E1%BA%A3m-10K-%C4%91%C6%A1n-0K-%C3%81o-thun-tay-l%E1%BB%A1-form-r%E1%BB%99ng-Oversize-%C3%A1o-ph%C3%B4ng-Unisex-si%C3%AAu-xinh-Pink-A368-i.385185467.4781860493",
#    "https://shopee.vn/-M%C3%A3-WASTNICE-gi%E1%BA%A3m-10-t%E1%BB%91i-%C4%91a-10K-%C4%91%C6%A1n-50K-%C3%81o-thun-tay-l%E1%BB%A1-form-r%E1%BB%99ng-Oversize-%C3%A1o-ph%C3%B4ng-Unisex-V%E1%BA%A3i-cotton-A265-i.385170418.7381841002",
#    "https://shopee.vn/%C3%81o-thun-Unisex-N7-Basic-Tee-ph%C3%B4ng-tr%C6%A1n-nam-n%E1%BB%AF-tay-l%E1%BB%A1-oversize-form-r%E1%BB%99ng-12-m%C3%A0u-i.257372007.3554096264",
#    "https://shopee.vn/%C3%81o-ph%C3%B4ng-unisex-nam-n%E1%BB%AF-form-r%E1%BB%99ng-tay-l%E1%BB%A1-ch%E1%BB%AF-SOUL-%C4%91%E1%BA%B9p-v%E1%BA%A3i-d%C3%A0y-m%E1%BB%8Bn-i.76875639.6855256837",
#    "https://shopee.vn/%C3%81o-thun-tay-l%E1%BB%A1-form-r%E1%BB%99ng-Oversize-%C3%A1o-ph%C3%B4ng-Unisex-V%E1%BA%A3i-cotton-A72-i.383842554.9425638636",
#    "https://shopee.vn/%C3%81o-Thun-Tay-L%E1%BB%A1-Nam-N%E1%BB%AF-Unisex-Form-R%E1%BB%99ng-%C3%81o-Ph%C3%B4ng-Tay-L%E1%BB%A1-Form-R%E1%BB%99ng-HAZA-UNISEX-ATL42-i.418264701.9037965893"
    "https://shopee.vn/%C4%90%E1%BB%93-ng%E1%BB%A7-n%E1%BB%AF-cotton-thun-c%E1%BB%99c-tay-pijama-%C4%90%E1%BB%93-b%E1%BB%99-n%E1%BB%AF-c%E1%BB%99c-tay-d%E1%BB%85-th%C6%B0%C6%A1ng-m%C3%B9a-h%C3%A8-ch%E1%BA%A5t-m%C3%A1t-nhi%E1%BB%81u-ho%E1%BA%A1-ti%E1%BA%BFt-%C4%91%E1%BA%B9p-i.146062031.7462059498",
    "https://shopee.vn/Set-%C4%91%E1%BB%93-n%E1%BB%AF-c%C3%A1-t%C3%ADnh-Ulzzang-%C4%91i-ch%C6%A1i-mua-h%C3%A8-gi%C3%A1-r%E1%BA%BB-%C3%81o-ph%C3%B4ng-tay-l%E1%BB%A1-qu%E1%BA%A7n-short-SNOOPY-SDN01-i.50982770.4284413167",
    "https://shopee.vn/%C4%90%E1%BB%93-B%E1%BB%99-Qu%E1%BA%A7n-%C3%81o-Th%E1%BB%83-Thao-Nam-M%C3%B9a-H%C3%A8-Ch%E1%BA%A5t-Thun-L%E1%BA%A1nh-Co-Gi%C3%A3n-4-Chi%E1%BB%81u-5-M%C3%A0u-SPORT-i.273744769.3010166114",
    "https://shopee.vn/B%E1%BB%99-%C4%91%E1%BB%93-ng%E1%BB%A7-n%E1%BB%AF-pijama-d%E1%BB%85-th%C6%B0%C6%A1ng-%C4%90%E1%BB%93-b%E1%BB%99-n%E1%BB%AF-cotton-thun-c%E1%BB%99c-tay-m%C3%B9a-h%C3%A8-ch%E1%BA%A5t-m%C3%A1t-nhi%E1%BB%81u-ho%E1%BA%A1-ti%E1%BA%BFt-%C4%91%E1%BA%B9p-BDN22-i.99635212.8934492513",
    "https://shopee.vn/B%E1%BB%99-%C4%91%E1%BB%93-ng%E1%BB%A7-g%E1%BB%93m-%C3%A1o-thun-ng%E1%BA%AFn-tay-v%C3%A0-qu%E1%BA%A7n-%C4%91%C3%B9i-th%E1%BB%9Di-trang-m%C3%B9a-h%C3%A8-tr%E1%BA%BB-trung-cho-n%E1%BB%AF-i.83082239.7461264370"

]

for url in shoppe_urls:
    saveDataShoppe(url)


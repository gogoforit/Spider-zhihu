from selenium import webdriver
import time
import information
from MongodbConn import MongoPipeline
def captcha1():#验证码输入
    try:
        driver.find_element_by_id('captcha')
        return True
    except:
        return False
def captcha2():#倒立的字
    try:
        driver.find_element_by_class_name('Captcha-imageConatiner')
        return True
    except:
        return False

if __name__ =="__main__":
# def send(urllist):
#     info = input("请输入搜索内容：\n")
    url1 = 'https://www.zhihu.com/people/wan-shi-xian-3/activities'


    driver = webdriver.Chrome(r'chromedriver.exe')
    url = 'https://www.zhihu.com/#signin'
    driver.get(url)
    driver.find_element_by_name('account').clear()
    driver.find_element_by_name('account').send_keys('') #账户
    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys('')#密码
    time.sleep(3)
    flag1 = captcha1()
    flag2 = captcha2()
    if flag1==True:
        k = input("请输入验证码,若无验证码，请输入“OK”:\n")
        try:
            driver.find_element_by_id('captcha').clear()
            driver.find_element_by_id('captcha').send_keys(k)
            driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/form/div[2]/button').click()
        except:
            driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/form/div[2]/button').click()
    elif flag2==True:
        k = input("请输入倒立的字，点击完成以后请输入“OK”，若无字，请直接输入“ok”\n")
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/form/div[2]/button').click()
        time.sleep(4)

    # driver.find_element_by_class_name('Icon Button-icon Icon--comments').click()
    # driver.find_element_by_css_selector('.MemberButtonGroup ProfileButtonGroup ProfileHeader-buttons').click()

    #开始发送私信
    # urllist = information.solve(info)
    conn = MongoPipeline()
    conn.open_connection('zhihu')
    ids = conn.getIds('info',{'type': 'url'})

    _id = next(ids, None)

    while _id:
        print(_id)
        url1 = _id['url']
        flag = _id['flag']
        _id = next(ids, None)
        if flag==False:
            time.sleep(2)
            driver.get(url1)
            time.sleep(5)
            mylist = driver.find_elements_by_tag_name('button')  #比较难定位，只能遍历所有标签，找到相同名字的
            for each in mylist:
                if each.text=='发私信':
                    each.click()
                    break
            mylist2 = driver.find_elements_by_tag_name('textarea')
            print(len(mylist2))
            print(mylist2[0].text)
            mylist2[0].clear()
            mylist2[0].send_keys('hello')
            # for each in mylist2:
            #     print(each.text)
            #     if each.text =='私信内容':
            #         each.clear()
            #         each.send_keys('hello')
            #         break
            mylist3 = driver.find_elements_by_tag_name('button')
            for each in mylist3:
                if each.text == '发送':
                    each.click()
                    break
            print('发送完成！...')

            conn.update_item({'url':url1},{"$set":{"flag":True}},'info')

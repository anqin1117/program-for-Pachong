import requests
import os
import time
from selenium import webdriver
import re
def save_image(url_list,image_class):
    #开始保存图片
    dir_name = os.getcwd() + '/' + image_class#生成类别文件夹
    isExists = os.path.exists(dir_name)
    if not isExists:#建立文件夹
        #print(dir_name)
        os.makedirs(dir_name)
        print('建立文件夹成功！')
    else:
        print('Dictionary areadly exists!')
    for i,url in enumerate(url_list):
        url = url.replace('amp;','')
        print('第%d张'%(i)+'正在保存\n'+url+'\n状态码：')
        r = requests.get(url)
        print(r.status_code)  # 返回状态码
        image_type = url.split('.')[-1]#生成图片类型
        if r.status_code == 200:
            open(dir_name + '/' + str(i) + '.' + image_type, 'wb').write(r.content)  # 将内容写入图片
            print("done")
        else:
            print("Status Code error!\nError code:" + r.status_code)
        del r
        time.sleep(1)#设置requests间隔防止被检测
def get_html(Keyword):#获取html
    print("正在采集页面信息....")
    url = 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=' + Keyword
    driver = webdriver.Chrome()#非谷歌浏览器请改下这里
    driver.get(url)
    time.sleep(1)
    #print(driver.page_source)
    #write_intext(driver.page_source)
    html1 = driver.execute_script("return document.documentElement.outerHTML")
    for _ in range(10):#模拟页面滑动 数值越大，爬的数据越多
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        driver.execute_script("var q=document.documentElement.scrollTop=0")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)  # 延时时间，为了能够让页面加载完全
    #print(1)
    html = driver.execute_script("return document.documentElement.outerHTML")
    if html1 == html:
        print('error!')
    #print(html)
    driver.quit()
    write_intext(html)
    return html
def write_intext(content):#写文件（测试用）
    f = open('html.txt', 'w', encoding='utf-8')
    f.write(content)
def get_image_url(html):#解析html，给出image url list
    print("正在解析html...")
    #f = open('html1.txt','r',encoding='utf-8')
    #html = f.read()
    #pattern = '"hoverURL":"(.*?)","pa'
    pattern = 'data-imgurl=".*?"src="(.*?)"'
    result = re.findall(pattern,html.replace(' ',''),re.DOTALL)
    print('解析完成！地址list如下：')
    print(result[6:])
    return result[6:]
if __name__ == '__main__':
    kw = '油画人物'#根据自己主题改这里
    html = get_html(kw)
    url_list = get_image_url(html)
    print(len(url_list))
    save_image(url_list,kw)

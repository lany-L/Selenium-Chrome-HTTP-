# Selenium-Chrome-HTTP-PROXY
Selenium使用谷歌插件实现账密代理

python安装依赖，填充代理信息，直接使用


  # 伪装真实设备UA，反爬虫,无需加载插件

```
  # https://bot.sannysoft.com/
  
  options.add_experimental_option(
      "excludeSwitches", ["enable-automation"])
  options.add_experimental_option('useAutomationExtension', False)
  options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
  options.add_argument(
      'user-agent=Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; EVA-AL00 Build/HUAWEIEVA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.14.0.2 Mobile Safari/537.36 AliApp(TB/7.7.5) UCBS/2.11.1.1 TTID/227200@taobao_android_7.7.5 WindVane/8.3.0 1080X1794')
  options.add_argument("disable-blink-features=AutomationControlled")  # 就是这一行告诉chrome去掉了webdriver痕迹

  driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        "source": "WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'Google Inc. (Intel)';}if (parameter === 37446) {return 'RENDERER_INPUT';}return getParameter(parameter);};"})
```


 # 记录一下，当你想在Selenium 自定义header，以下记录内容对你有帮助

```
#pip install --upgrade setuptools 
#pip install blinker==1.7.0 

# import the required library
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# define the request interceptor to configure custom headers
def interceptor(request):
    # add the missing headers
    request.headers["Accept-Language"] = "en-US,en;q=0.9"
    request.headers["Referer"] = "https://www.google.com/"

    # delete the existing misconfigured default headers values
    del request.headers["User-Agent"]
    del request.headers["Sec-Ch-Ua"]
    del request.headers["Sec-Fetch-Site"]
    del request.headers["Accept-Encoding"]

    # replace the deleted headers with edited values
    request.headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    request.headers["Sec-Ch-Ua"] = "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\""
    request.headers["Sec-Fetch-Site"] = "cross-site"
    request.headers["Accept-Encoding"] = "gzip, deflate, br, zstd"


# create a webdriver option
chrome_options = webdriver.ChromeOptions()

# run the browser in headless mode
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# start a Chrome instance
# driver = webdriver.Chrome(options=chrome_options)

# add the interceptor
driver.request_interceptor = interceptor

# open the target web page
driver.get("https://httpbin.io/headers")

# print the page source to view your request headers
print(driver.page_source)

# quit the driver
driver.quit()


```

# Selenium-Chrome-HTTP-PROXY
Selenium使用谷歌插件实现账密代理

python安装依赖，填充代理信息，直接使用


  # 伪装真实设备UA，反爬虫

```
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

import requests
proxies = {
  "http": "http://123.163.27.72",

}
response = requests.get("http://www.baidu.com", proxies=proxies)
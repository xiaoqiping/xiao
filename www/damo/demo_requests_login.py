from io import BytesIO

import requests
from PIL import Image


def LoginByPost():
    imgUrl='http://www.jzdzzj.cn/captcha/getcode?width=132&amp;height=54&amp;id=sign_in_1'
    s=requests.session()
    res=s.get(imgUrl,stream=True)


    im=Image.open(BytesIO(res.content))
    im.show()
    code=input()
    loginUrl='http://www.jzdzzj.cn/sign/account_sign_in_post.html'
    postData={'pname':'15019475691','password':'123456??','validateCode':code}
    rs=s.post(loginUrl,postData)
    url='http://www.jzdzzj.cn/consignment/consignment_info'
    res=s.get(url)
    res.encoding='utf-8'
    print(res.text)

LoginByPost()
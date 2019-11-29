from io import BytesIO

import requests
from PIL import Image
import tesserocr



def LoginByPost():
    imgUrl='http://www.jzdzzj.cn/captcha/getcode?width=132&amp;height=54&amp;id=sign_in_1'
    s=requests.session()
    res=s.get(imgUrl,stream=True)
    im=Image.open(BytesIO(res.content))
    im=im.convert('L')

    pixdata = im.load()
    w, h = im.size

    print(h)
    print(w)
    threshold = 180
    # 遍历所有像素，大于阈值的为黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    tesserocr.image_to_text(im)



LoginByPost()
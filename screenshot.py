import urllib.request, urllib.parse
import io, json
import base64
from PIL import ImageGrab


def get_access_token():
    """
    获取access_token
    apikey, secret_key由百度云api获取
    """
    apikey = ""
    secret_key = ""
    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (apikey,secret_key)
    request = urllib.request.Request(host)
    request.add_header("Content-Type", "application/json; charset=UTF-8")
    response = urllib.request.urlopen(request)
    content = response.read()   # 返回json格式数据
    # print(content)
    if content:
        q = json.loads(content.decode())
        return q["access_token"]
    return None


def clipboard():
    """
    从剪贴板获取图片信息
    """
    image = ImageGrab.grabclipboard()   # 返回模式为'RGB'的图像或者文件列表
    if image is None:
        print("剪贴板没有图片信息")
        return
    print('image size: %sx%s\n>>>\n' % (image.size[0], image.size[1]))
    b = io.BytesIO()
    image.save(b, "JPEG")   # 将image以jpeg格式存在b中
    b.seek(0)   # 绝对文件定位
    b64 = base64.encodebytes(b.read())
    access_token = get()    # 获取access_token
    if access_token is not None:
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s" % access_token
        data = urllib.parse.urlencode({'image': b64}).encode()
        request = urllib.request.Request(url, method="POST")
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(request, data=data) as f:
            response = f.read()
            r = json.loads(response)
            if r["words_result"] is not None:
                for m in r["words_result"]:
                    print(m["words"])
    else:
        print("access_token is none")


if __name__ == "__main__":
    print("运行后先截图再决定是否提取文字！")
    mes = input("请输入是否提取(y or n):  ")
    while(mes != "n"):
        if mes == "y":
            clipboard()
        mes = input("提取结束，是否继续： ")

import base64
import urllib
import requests
import json
import audio
import sj

API_KEY = "qNfurWpmi4kSBTnlleSGANjH"
SECRET_KEY = "iz0IUBEiGG5xO6sMtXq1K8IkvZ1giTGD"

def main():
        
    url = "https://vop.baidu.com/pro_api"
    
    # speech 可以通过 get_file_content_as_base64("C:\fakepath\test.wav",False) 方法获取

    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "DTSF",
        "token": get_access_token(),
        "dev_pid": 80001,
        "speech": get_file_content_as_base64("E:\\学习\\录音\\test.pcm",False) ,
        "len": 63532
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    
    #将识别结果进行切片，方便对比
    a=response.text
    a=a.split('[',2)
    a=a[1]
    a=a.split('。')
    a=a[0]
    a=a.split('\"')
    a=a[1]
    print(f"识别结果：{a}")
    if a=="关闭":
        return 0
    if a=="打开":
        return 1

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    response, master=sj.ConnectRelay("COM3")
    print(response)
    while(1):
        command = input("输入1录音，输入2退出：")
        if command=="1":
            #录音并识别
            #audio.start_audio()  
            p=main()
            if p==1:
                sj.Switch(master,"ON")
            elif p==0:
                sj.Switch(master,"OFF")
        elif command=="2":
            sj.Switch(master,"OFF")
            print("退出")
            break
       

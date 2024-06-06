import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import os
import time


def save_file(*args):
    # 获取当前工作目录
    current_working_directory = os.getcwd()
    #相对路径
    relative_path="output"
    #完整路径
    full_path = os.path.join(current_working_directory, relative_path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    global path
    path=full_path
    if len(args)>0: #1个参数返回目录路径
        return path
    else:           #无参数返回文件目录
        # 获取当前时间戳（秒）
        timestamp = int(time.time())
        # 使用时间戳来命名一个文件
        filename = f"{timestamp}.png"
        file_path = os.path.join(full_path, filename)
        return file_path

def has_new_photo():
    """
    检查自上次检查时间以来是否有新照片被添加到目录中。
    
    :param directory: 照片所在的目录路径
    :param last_check_time: 上次检查的时间戳（以秒为单位）
    :return: 如果有新照片则返回True，否则返回False
    """
    # 获取当前时间戳
    current_time = time.time()
    directory=save_file(1)
    last_check_time=current_time-5 #检测与上次相隔的时间
    # 列出目录中的所有文件
    for filename in os.listdir(directory):
        # 构建文件的完整路径
        file_path = os.path.join(directory, filename)
        
        # 检查文件是否是照片（可以根据文件扩展名或其他条件来判断）
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # 获取文件的修改时间戳
            file_mtime = os.path.getmtime(file_path)
            
            # 如果文件的修改时间晚于上次检查时间，说明有新照片
            if file_mtime > last_check_time:
                return True
    
    # 如果没有找到新照片，返回False
    return False

def overdraw(url,prompt,negative_prompt,steps,model):
    os.environ["http_proxy"] = "http://127.0.0.1:2080"
    os.environ["https_proxy"] = "http://127.0.0.1:2080"

    payload = {
        "prompt": f"{prompt}",
        "negative_prompt":f"{negative_prompt}",
        "steps": steps,
        "sampler_name": "DPM++ SDE Karras",
        "width": 480,
        "height": 640,
        "restore_faces": True
    }

    # 切换模型

    override_settings = {}
    override_settings["sd_model_checkpoint"] = f"{model}"
    override_payload = {
                    "override_settings": override_settings
                }
    payload.update(override_payload)

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    #保存图片
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        file_path=save_file()
        image.save(file_path, pnginfo=pnginfo)

if __name__ == "__main__":
    url = "http://119.23.213.95:8001"
    prompt="photo of beautiful age 18 girl, blonde hair, sexy,yellow"
    negative_prompt="text, watermark, low quality, medium quality, blurry, censored, wrinkles, deformed, mutated text, watermark, low quality, medium quality, blurry, censored, wrinkles, deformed, mutated"
    steps=20
    model=""
    overdraw(url,prompt,negative_prompt,steps,model)
    if has_new_photo():
        print('有新照片被添加')
    else:
        print('没有新照片被添加')

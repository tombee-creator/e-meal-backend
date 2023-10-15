import re
import pyocr
import base64
import numpy as np
import cv2
from PIL import Image

from .exceptions import *

class ReceiptConvertService:
    specific_words = ['小計', '税', '合計']
    
    def cv2pil(self, image):
        ''' OpenCV型 -> PIL型 '''
        new_image = image.copy()
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
        new_image = Image.fromarray(new_image)
        return new_image

    # base64で記述された画像をJSONに変換
    def convert(self, src_base64):
        img_binary = base64.b64decode(src_base64)
        jpg = np.frombuffer(img_binary, dtype=np.uint8)
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
        cv_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv_image = cv2.GaussianBlur(cv_image, (5, 5), 2)
        _, cv_image = cv2.threshold(cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        tools = pyocr.get_available_tools()
        tool = tools[0]

        str_jp = tool.image_to_string(
            self.cv2pil(cv_image),
            lang="jpn")
        txt_pyocr = str_jp.replace(' ', '')
        
        reciept = []
        for line in txt_pyocr.split("\n"):
            try:
                including_reserved_words = list(map(lambda reserved_words: line.find(reserved_words) != -1, ReceiptConvertService.specific_words))
                if any(including_reserved_words):
                    break
                match = re.search(r'([^ 　a-zA-Z0-9*%!\"\#\$\%\'\\]+)(\\([0-9]+))', line)
                if match == None:
                    continue
                name = match.groups()[0]
                cost = match.groups()[2]
                if name != None and cost != None and len(name) > 2 and len(name) < 13:
                    reciept.append({
                        'name': name,
                        'cost': int(cost)
                    })
            except:
                pass
        if len(reciept) == 0:
            raise CantFindValidDataError()
        return reciept

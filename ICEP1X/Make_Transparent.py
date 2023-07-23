import cv2
import numpy as np
from PIL import Image
trans = [0, 0, 0]
def transImage(image_path, final_image, trans=[0, 0, 0]):
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
  
        datas = img.getdata()
  
        newData = []
    
        for item in datas:
            if item[0] == trans[0] and item[1] == trans[1] and item[2] == trans[2]:
                newData.append((trans[0], trans[1], trans[2], 0))
            else:
                newData.append(item)
    
        img.putdata(newData)
        img.save(final_image, "PNG")
        return "Save Successful!"
    except Exception as e:
        return "Save Failed!\n"+str(e)
  

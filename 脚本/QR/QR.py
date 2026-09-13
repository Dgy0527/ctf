# 终端执行: pip install opencv-python

import cv2

# 图片放在同目录，文件名改为 qrcode.png
img = cv2.imread("qrcode.png")
detector = cv2.QRCodeDetector()

# 解码
data, bbox, _ = detector.detectAndDecode(img)

if bbox is not None:
    print(f"二维码内容：{data}")
else:
    print("没有识别到二维码")

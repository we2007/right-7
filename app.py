import cv2
import numpy as np

def extract_contours(image_path):
    # 读取图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 使用 Canny 边缘检测提取线条
    edges = cv2.Canny(image, 100, 200)

    # 找到轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

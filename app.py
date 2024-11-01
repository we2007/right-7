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
import cv2
import numpy as np

def apply_colors_to_contours(image_path, contours, colors):
    # 读取原始图像
    image = cv2.imread(image_path)
    
    # 检查图像是否成功加载
    if image is None:
        raise ValueError(f"Failed to load image from path: {image_path}")
    
    # 创建一个黑色背景的图像，用于绘制彩色线条
    neon_image = np.zeros_like(image)

    # 检查 colors 和 contours 数量是否一致，避免 IndexError
    if len(colors) != len(contours):
        raise ValueError("Number of colors and contours must be the same.")
    
    # 遍历每个轮廓，并应用用户选择的颜色
    for i, contour in enumerate(contours):
        color = colors[i]
        
        # 确保颜色是以 # 开头的六位十六进制颜色值
        if not color.startswith('#') or len(color) != 7:
            raise ValueError(f"Invalid color format: {color}. Expected format is '#RRGGBB'.")
        
        # 将颜色从十六进制转换为 BGR 格式 (OpenCV 使用 BGR 而非 RGB)
        try:
            bgr_color = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (4, 2, 0))
        except ValueError:
            raise ValueError(f"Invalid color value: {color}. Could not convert to BGR.")

        # 绘制轮廓
        cv2.drawContours(neon_image, [contour], -1, bgr_color, thickness=5)

    return neon_image
    

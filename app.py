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
   def add_neon_effect(image):
    # 创建发光效果：对图像进行多次模糊叠加
    for _ in range(3):
        blurred = cv2.GaussianBlur(image, (15, 15), 0)
        image = cv2.addWeighted(image, 0.6, blurred, 0.4, 0)
    
    return image      import os

def generate_final_neon_image(image_path, contours, color_data):
    # 提取轮廓并转换颜色数据为BGR格式
    colors = [color['color'] for color in color_data]
    
    # 应用颜色到轮廓
    neon_image = apply_colors_to_contours(image_path, contours, colors)
    
    # 添加霓虹灯发光效果
    neon_image_with_effect = add_neon_effect(neon_image)
    
    # 保存生成的图像 
    output_path = 'output/neon_final_image.jpg'
    cv2.imwrite(output_path, neon_image_with_effect)
    
    return output_path  
from flask import Flask, request, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)

# 上传图片并提取线条轮廓
@app.route('/process-image', methods=['POST'])
def process_image():
    file = request.files['image']
    image_path = os.path.join('uploads', file.filename)
    file.save(image_path)

    contours = extract_contours(image_path)
    
    # 将轮廓转换为 SVG 路径并返回给前端
    svg_paths = []
    for contour in contours:
        path = "M " + " ".join([f"{point[0][0]} {point[0][1]}" for point in contour])
        svg_paths.append(f'<path class="neon-path" d="{path}" stroke="#000" fill="none"/>')

    svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500">{"".join(svg_paths)}</svg>'
    
    return jsonify({'svg': svg_content, 'contours': contours})

# 提交用户选择的颜色并生成最终图像
@app.route('/submit-colors', methods=['POST'])
def submit_colors():
    color_data = request.json  # 从前端接收到的颜色数据
    image_path = 'path_to_uploaded_image'  # 之前上传的图像路径
    contours = extract_contours(image_path)

    # 生成最终的霓虹灯图像
    output_path = generate_final_neon_image(image_path, contours, color_data)

    return jsonify({'success': True, 'output_image': output_path})

if __name__ == '__main__':
    app.run(debug=True)

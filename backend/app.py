import json

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import time
import datetime
import glob

app = Flask(__name__)
CORS(app)

# 配置上传文件夹
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
PROCESSED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'processed')

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# 清理12小时前的图片
def clean_old_images():
    current_time = time.time()
    # 12小时的秒数
    time_threshold = 12 * 60 * 60
    
    # 清理上传文件夹
    for file_path in glob.glob(os.path.join(UPLOAD_FOLDER, '*')):
        # 获取文件的创建时间
        file_creation_time = os.path.getctime(file_path)
        # 如果文件创建时间超过12小时
        if current_time - file_creation_time > time_threshold:
            try:
                os.remove(file_path)
                print(f"已删除旧文件: {file_path}")
            except Exception as e:
                print(f"删除文件失败: {file_path}, 错误: {str(e)}")
    
    # 清理处理后的文件夹
    for file_path in glob.glob(os.path.join(PROCESSED_FOLDER, '*')):
        file_creation_time = os.path.getctime(file_path)
        if current_time - file_creation_time > time_threshold:
            try:
                os.remove(file_path)
                print(f"已删除旧文件: {file_path}")
            except Exception as e:
                print(f"删除文件失败: {file_path}, 错误: {str(e)}")

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 处理图片，去除上下黑边
def process_image(image_path, output_path):
    print("处理图片")
    # 打开图片
    img = Image.open(image_path).convert("RGB")
    np_img = np.array(img)

    # 获取图像高度和宽度
    h, w, _ = np_img.shape

    # 获取灰度图，用于判断“黑”区域
    gray = np.mean(np_img, axis=2)

    # 设置黑色的判断阈值（0~255），越低越严格
    black_threshold = 0

    # 找出非黑行的索引（上下）
    non_black_rows = np.where(np.min(gray, axis=1) > black_threshold)[0]

    if non_black_rows.size == 0:
        print("找不到非黑区域")
        return False

    top, bottom = non_black_rows[0], non_black_rows[-1]

    # 裁剪并保存
    cropped_img = img.crop((0, top, w, bottom + 1))  # (left, upper, right, lower)
    cropped_img.save(output_path)
    print("处理图片结束")
    return True

@app.route('/upload', methods=['POST'])
def upload_file():
    # 清理旧图片
    clean_old_images()
    
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            # 生成安全的文件名
            filename = secure_filename(file.filename)
            # 添加时间戳和UUID以确保唯一性
            unique_filename = f"{int(time.time())}_{uuid.uuid4().hex}_{filename}"
            
            # 保存原始文件
            upload_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(upload_path)
            
            # 处理图片
            processed_filename = f"processed_{unique_filename}"
            processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
            
            try:
                process_image(upload_path, processed_path)
                
                # 构建下载URL
                download_url = f"/download/{processed_filename}"
                original_url = f"/download/{unique_filename}"
                
                results.append({
                    'original_name': unique_filename,
                    'display_name': file.filename,
                    'processed_name': processed_filename,
                    'download_url': download_url,
                    'original_url': original_url
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': f'File {file.filename} not allowed'}), 400
    print(f"处理图片完成{results}")
    return jsonify({'message': 'Files processed successfully', 'results': results})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # 检查是否是处理后的图片
    if filename.startswith('processed_'):
        return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)
    else:
        # 返回原始图片
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route('/test/<name>', methods=['GET'])
def test_methods(name):
    obj = {'name':name}
    return json.dumps(obj)

if __name__ == '__main__':
    # 应用启动时清理旧图片
    clean_old_images()
    app.run(debug=True, host='0.0.0.0', port=5001)
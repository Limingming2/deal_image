# 图片处理网站

这是一个批量上传图片并处理的网站。用户可以上传图片，服务端会自动去除图片上下方的黑色部分，然后提供处理后图片的下载链接。

## 项目结构

```
deal_image/
├── backend/             # Python后端
│   ├── app.py           # 主应用程序
│   ├── requirements.txt # 依赖包列表
│   ├── uploads/         # 原始图片上传目录
│   └── processed/       # 处理后图片存储目录
└── frontend/            # Vue3前端
    ├── public/
    ├── src/
    ├── package.json
    └── vite.config.js
```

## 功能特点

- 批量上传图片
- 自动去除图片上下方的黑色部分
- 提供处理后图片的下载链接
- 响应式设计，适配不同设备

## 安装与运行

### 后端

1. 进入后端目录
   ```
   cd backend
   ```

2. 安装依赖
   ```
   pip install -r requirements.txt
   ```

3. 运行服务
   ```
   python app.py
   ```
   服务将在 http://localhost:5000 运行

### 前端

1. 进入前端目录
   ```
   cd frontend
   ```

2. 安装依赖
   ```
   npm install
   ```

3. 开发模式运行
   ```
   npm run dev
   ```
   前端将在 http://localhost:3000 运行

4. 构建生产版本
   ```
   npm run build
   ```

## 使用方法

1. 打开网站首页
2. 点击上传区域或拖拽图片到上传区域
3. 选择需要处理的图片（支持批量选择）
4. 等待图片上传和处理完成
5. 点击下载链接获取处理后的图片
<template>
  <div class="home-container">
    <header class="header">
      <h1>图片处理工具</h1>
      <p>自动去除图片上下方的黑色部分</p>
    </header>

    <main class="main-content">
      <el-card class="upload-card">
        <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
          <input
            type="file"
            ref="fileInput"
            multiple
            accept="image/*"
            style="display: none"
            @change="handleFileChange"
          />
          <el-icon class="upload-icon"><Upload /></el-icon>
          <div class="upload-text">
            <span>点击或拖拽图片到此区域上传</span>
            <p class="upload-hint">支持批量上传多个图片文件</p>
          </div>
        </div>

        <div v-if="uploadStatus.uploading" class="upload-progress">
          <el-progress :percentage="uploadStatus.progress" />
          <p>正在上传和处理图片，请稍候...</p>
        </div>

        <div v-if="selectedFile" class="preview-section">
          <h3>图片预览</h3>
          <ImageComparison 
            :original-url="selectedFile.originalPreviewUrl" 
            :processed-url="selectedFile.processedPreviewUrl"
            message="选择一个处理后的图片查看对比效果"
          />
        </div>

        <div v-if="uploadedFiles.length > 0" class="result-list">
          <h3>处理结果</h3>
          <el-table :data="uploadedFiles" style="width: 100%">
            <el-table-column prop="display_name" label="原始文件名" width="180" />
            <el-table-column label="操作" width="200">
              <template #default="scope">
                <el-button type="primary" size="small" @click="previewFile(scope.row)">
                  预览
                </el-button>
                <el-button type="success" size="small" @click="downloadFile(scope.row.download_url)">
                  下载
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </main>

    <footer class="footer">
      <p>© {{ new Date().getFullYear() }} 图片处理工具</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import ImageComparison from '../components/ImageComparison.vue'

const fileInput = ref(null)
const uploadedFiles = ref([])
const selectedFile = ref(null)
const uploadStatus = reactive({
  uploading: false,
  progress: 0
})

// 触发文件选择框
const triggerFileInput = () => {
  fileInput.value.click()
}

// 处理文件选择
const handleFileChange = (event) => {
  const files = event.target.files
  if (files && files.length > 0) {
    uploadFiles(files)
  }
}

// 处理拖放上传
const handleDrop = (event) => {
  const files = event.dataTransfer.files
  if (files && files.length > 0) {
    uploadFiles(files)
  }
}

// 上传文件到服务器
const uploadFiles = async (files) => {
  if (!files || files.length === 0) return

  // 检查文件类型
  const validFiles = Array.from(files).filter(file => {
    const isValid = file.type.startsWith('image/')
    if (!isValid) {
      ElMessage.error(`${file.name} 不是有效的图片文件`)
    }
    return isValid
  })

  if (validFiles.length === 0) return

  uploadStatus.uploading = true
  uploadStatus.progress = 0

  const formData = new FormData()
  validFiles.forEach(file => {
    formData.append('files', file)
  })

  try {
    // 模拟上传进度
    const progressInterval = setInterval(() => {
      if (uploadStatus.progress < 90) {
        uploadStatus.progress += 10
      }
    }, 300)

    const response = await axios.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    clearInterval(progressInterval)
    uploadStatus.progress = 100

    setTimeout(() => {
      uploadStatus.uploading = false
      if (response.data && response.data.results) {
        uploadedFiles.value = response.data.results
        ElMessage.success('图片处理成功')
      }
    }, 500)
  } catch (error) {
    uploadStatus.uploading = false
    console.error('上传失败:', error)
    ElMessage.error('上传失败: ' + (error.response?.data?.error || error.message || '未知错误'))
  }

  // 清空文件输入，允许重新选择相同文件
  fileInput.value.value = ''
}

// 预览文件
const previewFile = (file) => {
  // 使用后端提供的URL，确保通过API代理
  const originalUrl = `/api${file.original_url}`
  const processedUrl = `/api${file.download_url}`
  
  selectedFile.value = {
    originalPreviewUrl: originalUrl,
    processedPreviewUrl: processedUrl,
    ...file
  }
}

// 下载处理后的文件
const downloadFile = (url) => {
  // 确保通过API代理访问后端
  const apiUrl = url.startsWith('/api') ? url : `/api${url}`
  window.open(apiUrl, '_blank')
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  text-align: center;
  padding: 2rem 0;
  background-color: #409eff;
  color: white;
}

.header h1 {
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

.upload-card {
  margin-bottom: 2rem;
}

.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  padding: 3rem 0;
  text-align: center;
  transition: border-color 0.3s;
}

.upload-area:hover {
  border-color: #409eff;
}

.upload-icon {
  font-size: 4rem;
  color: #8c939d;
  margin-bottom: 1rem;
}

.upload-text {
  color: #606266;
}

.upload-hint {
  font-size: 0.9rem;
  color: #909399;
  margin-top: 0.5rem;
}

.upload-progress {
  margin-top: 1.5rem;
  text-align: center;
}

.result-list {
  margin-top: 2rem;
}

.result-list h3 {
  margin-bottom: 1rem;
  font-weight: 500;
  color: #303133;
}

.footer {
  text-align: center;
  padding: 1.5rem 0;
  background-color: #f5f7fa;
  color: #909399;
  font-size: 0.9rem;
}
</style>
<template>
  <div class="image-comparison-container">
    <div v-if="originalUrl && processedUrl" class="comparison-view">
      <div class="image-container">
        <h4>原始图片</h4>
        <img :src="originalUrl" alt="原始图片" class="comparison-image" />
      </div>
      <div class="image-container">
        <h4>处理后图片</h4>
        <img :src="processedUrl" alt="处理后图片" class="comparison-image" />
      </div>
    </div>
    <div v-else class="no-image">
      <p>{{ message || '暂无图片可供比较' }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, watch } from 'vue';

const props = defineProps({
  originalUrl: String,
  processedUrl: String,
  message: String
});

</script>

<style scoped>
.image-comparison-container {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f9f9f9;
}

.comparison-view {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem;
}

.image-container {
  flex: 1;
  min-width: 300px;
  text-align: center;
}

.image-container h4 {
  margin-bottom: 0.5rem;
  color: #606266;
}

.comparison-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.no-image {
  padding: 2rem;
  text-align: center;
  color: #909399;
}
</style>
<script setup lang="ts">
import LoadingDots from '@/components/common/LoadingDots.vue'

defineProps<{
  content: string
  isGenerating: boolean
  currentStep: number
  isLoading: boolean
}>()

const emit = defineEmits<{
  'download-xmind': []
  'save-xmind': []
}>()
</script>

<template>
  <div class="outline-section">
    <h3 class="section-title">大纲</h3>
    <div class="outline-content">
      <LoadingDots v-if="isGenerating && !content" text="生成中..." />
      <div v-if="content" class="outline-text">{{ content }}</div>
      <LoadingDots v-if="isGenerating && content" text="继续生成中..." />
      <div v-if="!isGenerating && !content" class="empty-hint">
        <p>文件已上传</p>
        <p class="hint-text">按回车键生成大纲</p>
      </div>
    </div>

    <div v-if="currentStep >= 2" class="outline-action">
      <div v-if="currentStep === 2" class="action-row">
        <button
          class="icon-btn"
          title="生成 XMind"
          @click="emit('download-xmind')"
          :disabled="isLoading"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
          </svg>
        </button>
        <span class="action-label">{{ isLoading ? '生成中...' : '生成 XMind' }}</span>
      </div>
      <div v-else class="action-row">
        <div class="done-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          XMind 已生成
        </div>
        <button
          class="icon-btn download-btn"
          title="下载 XMind"
          @click="emit('save-xmind')"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.outline-section {
  flex: 1;
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  overflow-y: auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e5e7eb;
}

.outline-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.outline-text {
  color: #374151;
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-wrap;
}

.empty-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #9ca3af;
}

.empty-hint p {
  font-size: 14px;
  margin: 4px 0;
}

.hint-text {
  font-size: 12px;
  color: #d1d5db;
}

.outline-action {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: center;
}

.action-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-label {
  font-size: 14px;
  color: #4b5563;
  font-weight: 500;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #ffffff;
  color: #7c3aed;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.icon-btn svg {
  width: 18px;
  height: 18px;
}

.icon-btn:hover:not(:disabled) {
  background: #f5f3ff;
  border-color: #7c3aed;
}

.icon-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon-btn.download-btn {
  color: #10b981;
}

.icon-btn.download-btn:hover {
  background: #ecfdf5;
  border-color: #10b981;
}

.done-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #10b981;
  font-weight: 500;
}

.done-badge svg {
  width: 16px;
  height: 16px;
}
</style>

<script setup lang="ts">
defineProps<{
  currentStep: number
  isLoading: boolean
}>()

const emit = defineEmits<{
  'download-csv': []
  'save-csv': []
  'save-xmind': []
}>()
</script>

<template>
  <div class="file-panel">
    <h3 class="section-title">文件</h3>

    <div class="file-card">
      <div class="file-card-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
          <polyline points="10 9 9 9 8 9" />
        </svg>
      </div>
      <div class="file-card-info">
        <span class="file-card-name">思维导图.xmind</span>
        <span class="file-card-status">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          已生成
        </span>
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

    <div v-if="currentStep === 3" class="file-action">
      <div class="action-row">
        <button
          class="icon-btn"
          title="生成 CSV"
          @click="emit('download-csv')"
          :disabled="isLoading"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
          </svg>
        </button>
        <span class="action-label">{{ isLoading ? '生成中...' : '生成 CSV' }}</span>
      </div>
    </div>

    <div v-if="currentStep >= 4" class="file-card">
      <div class="file-card-icon csv">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
        </svg>
      </div>
      <div class="file-card-info">
        <span class="file-card-name">测试用例.csv</span>
        <span class="file-card-status">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          已生成
        </span>
      </div>
      <button
        class="icon-btn download-btn"
        title="下载 CSV"
        @click="emit('save-csv')"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="7 10 12 15 17 10" />
          <line x1="12" y1="15" x2="12" y2="3" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.file-panel {
  width: 320px;
  min-width: 280px;
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  min-height: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  padding-bottom: 8px;
  border-bottom: 2px solid #e5e7eb;
}

.file-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  transition: all 0.2s;
}

.file-card:hover {
  border-color: #c4b5fd;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.08);
}

.file-card-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #ede9fe;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.file-card-icon svg {
  width: 22px;
  height: 22px;
  color: #7c3aed;
}

.file-card-icon.csv {
  background: #ecfdf5;
}

.file-card-icon.csv svg {
  color: #10b981;
}

.file-card-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  flex: 1;
}

.file-card-name {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-card-status {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #10b981;
}

.file-card-status svg {
  width: 14px;
  height: 14px;
}

.file-action {
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
  margin-left: auto;
}

.icon-btn.download-btn:hover {
  background: #ecfdf5;
  border-color: #10b981;
}

@media (max-width: 1024px) {
  .file-panel {
    width: 100%;
    min-width: auto;
  }
}
</style>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  currentStep: number
  isLoading: boolean
  isGeneratingOutline: boolean
  modelValue: string
  uploadedFile: File | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  'file-upload': [event: Event]
  'remove-file': []
  'generate-outline': []
  keydown: [event: KeyboardEvent]
}>()

const fileInputRef = ref<HTMLInputElement | null>(null)

function triggerFileUpload() {
  fileInputRef.value?.click()
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}
</script>

<template>
  <div class="input-container">
    <div v-if="uploadedFile" class="file-preview">
      <div class="file-chip">
        <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
        </svg>
        <span class="file-name">{{ uploadedFile.name }}</span>
        <span class="file-size">{{ formatFileSize(uploadedFile.size) }}</span>
        <button
          class="file-remove-btn"
          title="移除文件"
          aria-label="移除文件"
          @click="emit('remove-file')"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
    </div>

    <div class="input-wrapper">
      <div class="input-actions-left">
        <button class="action-btn" title="上传文件" aria-label="上传文件" @click="triggerFileUpload">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
        </button>
        <input
            ref="fileInputRef"
            type="file"
            class="file-input-hidden"
            accept=".md,.docx,.pdf"
            @change="(e) => emit('file-upload', e)"
        />
      </div>

      <textarea
          class="message-input"
          placeholder="上传文件后按回车生成大纲..."
          rows="1"
          :value="modelValue"
          @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
          @keydown="emit('keydown', $event)"
          :disabled="isLoading || currentStep === 0"
          aria-label="消息输入框"
      ></textarea>

      <div class="input-actions-right">
        <button
            v-if="currentStep === 1"
            class="send-btn"
            aria-label="生成大纲"
            @click="emit('generate-outline')"
            :disabled="isLoading || isGeneratingOutline"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.input-container {
  max-width: 100%;
}

.file-preview {
  padding: 0 8px 8px;
}

.file-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f0ebff;
  border: 1px solid #d8ccf8;
  border-radius: 10px;
  font-size: 13px;
  color: #5b21b6;
}

.file-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: #7c3aed;
}

.file-name {
  font-weight: 500;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  color: #8b5cf6;
  font-size: 12px;
}

.file-remove-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: none;
  background: transparent;
  color: #8b5cf6;
  cursor: pointer;
  border-radius: 4px;
  padding: 0;
  transition: all 0.2s;
}

.file-remove-btn:hover {
  background: #ddd6fe;
  color: #5b21b6;
}

.file-remove-btn svg {
  width: 14px;
  height: 14px;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  padding: 16px 20px;
  background: #ffffff;
  border: 2px solid transparent;
  border-image: linear-gradient(to right, #d8b4e2, #a8c0f2) 1;
  border-radius: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.input-wrapper:focus-within {
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.15);
}

.input-actions-left,
.input-actions-right {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.file-input-hidden {
  display: none;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.action-btn svg {
  width: 20px;
  height: 20px;
}

.message-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  color: #1f2937;
  resize: none;
  min-height: 24px;
  max-height: 200px;
  line-height: 1.5;
  font-family: inherit;
}

.message-input::placeholder {
  color: #9ca3af;
}

.message-input:disabled {
  background: transparent;
  cursor: not-allowed;
}

.send-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  background: #7c3aed;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  background: #6d28d9;
  transform: scale(1.05);
}

.send-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

.send-btn svg {
  width: 20px;
  height: 20px;
}
</style>

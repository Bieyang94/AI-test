<script setup lang="ts">
import { ref } from 'vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import StepIndicator from '@/components/common/StepIndicator.vue'
import OutlinePanel from '@/components/chat/OutlinePanel.vue'
import ActionPanel from '@/components/chat/ActionPanel.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
import { useFileWorkflow } from '@/composables/useFileWorkflow'

interface Conversation {
  id: string
  title: string
  date: Date
}

const conversations = ref<Conversation[]>([
  { id: '1', title: '第一次对话', date: new Date() },
  { id: '2', title: '关于API的讨论', date: new Date() },
])

const {
  currentStep,
  uploadedFile,
  outlineContent,
  isGeneratingOutline,
  isLoading,
  messageInput,
  getStepDescription,
  reset,
  handleRemoveFile,
  handleFileUpload,
  handleGenerateOutline,
  handleDownloadXmind,
  handleDownloadCsv,
  handleSaveXmind,
  handleSaveCsv,
  handleKeydown,
} = useFileWorkflow()

function selectConversation(id: string) {
  console.log('选择对话:', id)
}
</script>

<template>
  <div class="chat-container">
    <AppSidebar
      :conversations="conversations"
      @new-conversation="reset"
      @select-conversation="selectConversation"
    />

    <main class="main-content">
      <StepIndicator v-if="currentStep > 0" :description="getStepDescription()" />

      <div v-if="currentStep > 0" class="content-area">
        <OutlinePanel
          :content="outlineContent"
          :is-generating="isGeneratingOutline"
          :current-step="currentStep"
          :is-loading="isLoading"
          @download-xmind="handleDownloadXmind"
          @save-xmind="handleSaveXmind"
        />
        <ActionPanel
          v-if="currentStep >= 3"
          :current-step="currentStep"
          :is-loading="isLoading"
          @download-csv="handleDownloadCsv"
          @save-csv="handleSaveCsv"
          @save-xmind="handleSaveXmind"
        />
      </div>
      <div v-else class="empty-spacer"></div>

      <ChatInput
        v-model="messageInput"
        :current-step="currentStep"
        :is-loading="isLoading"
        :is-generating-outline="isGeneratingOutline"
        :uploaded-file="uploadedFile"
        @file-upload="handleFileUpload"
        @remove-file="handleRemoveFile"
        @generate-outline="handleGenerateOutline"
        @keydown="handleKeydown"
      />
    </main>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #ffffff;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 40px;
  position: relative;
  overflow: hidden;
}

.content-area {
  flex: 1;
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  overflow: hidden;
}

.empty-spacer {
  flex: 1;
}

@media (max-width: 1024px) {
  .content-area {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 20px;
  }

  .welcome-message p {
    font-size: 16px;
  }
}
</style>

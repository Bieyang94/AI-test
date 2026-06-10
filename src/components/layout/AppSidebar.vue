<script setup lang="ts">
import { ref } from 'vue'

interface Conversation {
  id: string
  title: string
  date: Date
}

defineProps<{
  conversations: Conversation[]
}>()

const emit = defineEmits<{
  'new-conversation': []
  'select-conversation': [id: string]
}>()

const expanded = ref(true)

function toggleExpand() {
  expanded.value = !expanded.value
}
</script>

<template>
  <aside class="sidebar">
    <div class="logo-section">
      <div class="logo-icon">
        <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="40" height="40" rx="8" fill="url(#sidebar-gradient)" />
          <path d="M12 14L20 10L28 14V22L20 26L12 22V14Z" fill="white" opacity="0.9" />
          <path d="M20 18L24 20V24L20 26L16 24V20L20 18Z" fill="white" />
          <defs>
            <linearGradient id="sidebar-gradient" x1="0" y1="0" x2="40" y2="40">
              <stop stop-color="#7C3AED" />
              <stop offset="1" stop-color="#4F46E5" />
            </linearGradient>
          </defs>
        </svg>
      </div>
      <span class="logo-text">CheryGPT <span class="version">3.0</span></span>
      <div class="header-action">
        <button class="icon-btn" title="帮助" aria-label="帮助">H</button>
      </div>
    </div>

    <button class="new-chat-btn" @click="emit('new-conversation')">
      <span class="plus-icon">+</span>
      <span>新对话</span>
    </button>

    <button class="menu-item">
      <svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" />
        <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
      </svg>
      <span>探索</span>
    </button>

    <div class="conversation-section">
      <button class="menu-item conversation-header" @click="toggleExpand">
        <svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
        <span>近期对话</span>
        <svg
            class="expand-icon"
            :class="{ expanded: expanded }"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      <transition name="slide">
        <div v-if="expanded" class="conversation-list">
          <div
              v-for="conv in conversations"
              :key="conv.id"
              class="conversation-item"
              @click="emit('select-conversation', conv.id)"
          >
            {{ conv.title }}
          </div>
        </div>
      </transition>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background-color: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
}

.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  margin-bottom: 16px;
}

.logo-icon svg {
  width: 40px;
  height: 40px;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.logo-text .version {
  color: #7c3aed;
  font-weight: 700;
}

.header-action {
  margin-left: auto;
}

.icon-btn {
  width: 28px;
  height: 28px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #ffffff;
  color: #6b7280;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.new-chat-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #ffffff;
  color: #7c3aed;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.new-chat-btn:hover {
  background: #f9fafb;
  border-color: #7c3aed;
}

.plus-icon {
  font-size: 18px;
  font-weight: 600;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  width: 100%;
}

.menu-item:hover {
  background: #f3f4f6;
}

.menu-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.conversation-section {
  margin-top: 8px;
}

.conversation-header {
  justify-content: space-between;
}

.expand-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.2s;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

.conversation-list {
  margin-top: 8px;
  padding-left: 12px;
}

.conversation-item {
  padding: 8px 12px;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conversation-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 768px) {
  .sidebar {
    width: 200px;
    padding: 16px;
  }
}
</style>

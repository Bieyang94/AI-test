<script setup lang="ts">
defineProps<{
  text?: string
}>()
</script>

<template>
  <div class="loading-container" role="status" aria-live="polite">
    <span class="loading-dot"></span>
    <span class="loading-dot"></span>
    <span class="loading-dot"></span>
    <span class="loading-text">{{ text ?? '加载中...' }}</span>
  </div>
</template>

<style scoped>
.loading-container {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px;
}

.loading-dot {
  width: 8px;
  height: 8px;
  background: #7c3aed;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.loading-dot:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dot:nth-child(2) {
  animation-delay: -0.16s;
}

.loading-text {
  color: #7c3aed;
  font-size: 14px;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
</style>

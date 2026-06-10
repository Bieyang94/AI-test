<script setup lang="ts">
defineProps<{
  description: string
}>()
</script>

<template>
  <div class="step-indicator" role="status" aria-live="polite">
    <span class="step-text">{{ description }}</span>
  </div>
</template>

<style scoped>
.step-indicator {
  margin-bottom: 20px;
  text-align: center;
}

.step-text {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}
</style>

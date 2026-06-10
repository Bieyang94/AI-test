<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="not-found">
    <h1>404</h1>
    <p>页面未找到</p>
    <button @click="router.push('/')">返回首页</button>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  gap: 16px;
}

.not-found h1 {
  font-size: 72px;
  color: #7c3aed;
}

.not-found p {
  font-size: 18px;
  color: #6b7280;
}

.not-found button {
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  background: #7c3aed;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.not-found button:hover {
  background: #6d28d9;
}
</style>

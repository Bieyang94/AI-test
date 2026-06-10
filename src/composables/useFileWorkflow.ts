import { ref, nextTick } from 'vue'
import { uploadFile, generateOutline, downloadXmind, downloadCsv } from '@/api'
import type { OutlineChunk, OutlineDone, OutlineError } from '@/api'
import { message } from '@/utils/message'

export function useFileWorkflow() {
    const currentStep = ref(0)
    const uploadedFile = ref<File | null>(null)
    const uploadedFileNum = ref(0)
    const outlineContent = ref('')
    const isGeneratingOutline = ref(false)
    const isLoading = ref(false)
    const messageInput = ref('')
    const xmindBlob = ref<Blob | null>(null)
    const xmindFilename = ref('')
    const csvBlob = ref<Blob | null>(null)
    const csvFilename = ref('')

    const STEP_DESCRIPTIONS: Record<number, string> = {
        1: '文件已上传，按回车生成大纲',
        2: '大纲已生成',
        3: 'XMind已生成',
        4: '完成',
    }

    function getStepDescription(): string {
        return STEP_DESCRIPTIONS[currentStep.value] ?? '完成'
    }

    function reset() {
        outlineContent.value = ''
        currentStep.value = 0
        uploadedFile.value = null
        uploadedFileNum.value = 0
        messageInput.value = ''
        xmindBlob.value = null
        xmindFilename.value = ''
        csvBlob.value = null
        csvFilename.value = ''
    }

    function handleRemoveFile() {
        uploadedFile.value = null
        currentStep.value = 0
        messageInput.value = ''
    }

    async function handleFileUpload(event: Event) {
        const target = event.target as HTMLInputElement
        const file = target.files?.[0]
        if (!file) return

        uploadedFile.value = file
        isLoading.value = true

        try {
            const res = await uploadFile(file, uploadedFileNum.value)
            uploadedFileNum.value = res.num
            messageInput.value = ''
            currentStep.value = 1
            message.success('文件上传成功')
        } catch (error: unknown) {
            const status = (error as { response?: { status?: number } })?.response?.status
            if (status === 400) {
                message.error('文件格式不支持或文件名为空')
            } else if (status === 422) {
                message.error('参数错误，请检查文件')
            } else {
                message.error('文件上传失败，请重试')
            }
        } finally {
            isLoading.value = false
            target.value = ''
        }
    }

    async function handleGenerateOutline() {
        if (currentStep.value !== 1) return

        isGeneratingOutline.value = true
        outlineContent.value = ''

        try {
            await generateOutline(
                uploadedFileNum.value,
                async (chunk: OutlineChunk) => {
                    outlineContent.value += chunk.content
                    await nextTick()
                },
                async (done: OutlineDone) => {
                    outlineContent.value += `\n\n(大纲生成完成，总长度: ${done.total_length} 字符)`
                    currentStep.value = 2
                    isGeneratingOutline.value = false
                    message.success('大纲生成完成')
                },
                async (err: OutlineError) => {
                    outlineContent.value = `生成失败: ${err.error}`
                    isGeneratingOutline.value = false
                    message.error('大纲生成失败')
                }
            )
        } catch {
            outlineContent.value = '生成大纲失败，请重试'
            isGeneratingOutline.value = false
            message.error('生成大纲失败，请重试')
        }
    }

    async function handleDownloadXmind() {
        if (currentStep.value !== 2) return
        isLoading.value = true
        try {
            const result = await downloadXmind(uploadedFileNum.value)
            xmindBlob.value = result.blob
            xmindFilename.value = result.filename
            currentStep.value = 3
            message.success('XMind 生成成功')
        } catch {
            message.error('XMind 文件生成失败')
        } finally {
            isLoading.value = false
        }
    }

    async function handleDownloadCsv() {
        if (currentStep.value !== 3) return
        isLoading.value = true
        try {
            const result = await downloadCsv(uploadedFileNum.value)
            csvBlob.value = result.blob
            csvFilename.value = result.filename
            currentStep.value = 4
            message.success('CSV 生成成功')
        } catch {
            message.error('CSV 文件生成失败')
        } finally {
            isLoading.value = false
        }
    }

    function saveBlob(blob: Blob, filename: string) {
        const objectUrl = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = objectUrl
        link.download = filename
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(objectUrl)
    }

    function handleSaveXmind() {
        if (xmindBlob.value && xmindFilename.value) {
            saveBlob(xmindBlob.value, xmindFilename.value)
            message.success('XMind 下载成功')
        }
    }

    function handleSaveCsv() {
        if (csvBlob.value && csvFilename.value) {
            saveBlob(csvBlob.value, csvFilename.value)
            message.success('CSV 下载成功')
        }
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            if (currentStep.value === 1) {
                handleGenerateOutline()
            }
        }
    }

    return {
        currentStep,
        uploadedFile,
        uploadedFileNum,
        outlineContent,
        isGeneratingOutline,
        isLoading,
        messageInput,
        xmindBlob,
        xmindFilename,
        csvBlob,
        csvFilename,
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
    }
}

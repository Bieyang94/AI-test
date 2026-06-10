import request from '../utils/request'

export interface UploadResponse {
    num: number
    ext: string
    text_length: number
    message: string
}

export interface OutlineChunk {
    index: number
    content: string
}

export interface OutlineDone {
    status: string
    num: number
    total_length: number
}

export interface OutlineError {
    error: string
}

export function uploadFile(file: File, num: number): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)

    return request.post(`/upload?num=${num}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
}

const getSseBaseUrl = (): string => import.meta.env.VITE_SSE_BASE_URL || ''

export async function generateOutline(
    num: number,
    onChunk: (chunk: OutlineChunk) => void,
    onDone: (done: OutlineDone) => void,
    onError: (error: OutlineError) => void
): Promise<void> {
    const response = await fetch(`${getSseBaseUrl()}/file/generateOutline?num=${num}`, {
        method: 'POST',
    })

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
        throw new Error('无法读取响应流')
    }

    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
            if (line.startsWith('event:')) continue

            if (line.startsWith('data:')) {
                const dataStr = line.slice(5).trim()
                if (!dataStr) continue

                try {
                    const data = JSON.parse(dataStr)
                    if (data.index !== undefined) {
                        onChunk(data as OutlineChunk)
                    } else if (data.status === 'done') {
                        onDone(data as OutlineDone)
                    } else if (data.error) {
                        onError(data as OutlineError)
                    }
                } catch {
                    console.error('解析SSE数据失败')
                }
            }
        }
    }
}

async function downloadFile(url: string, defaultFilename: string): Promise<{ blob: Blob; filename: string }> {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 120000)

    try {
        const response = await fetch(`${getSseBaseUrl()}${url}`, {
            method: 'POST',
            signal: controller.signal,
        })

        clearTimeout(timeoutId)

        if (response.status !== 201) {
            if (response.status === 404) {
                throw new Error(response.status === 404 ? '前置步骤未完成' : '资源未找到')
            }
            throw new Error(`HTTP error! status: ${response.status}`)
        }

        const contentDisposition = response.headers.get('Content-Disposition')
        let filename = defaultFilename

        if (contentDisposition) {
            const match = contentDisposition.match(/filename="?([^"]+)"?/)
            if (match?.[1]) filename = match[1]
        }

        const blob = await response.blob()
        return { blob, filename }
    } catch (error: unknown) {
        clearTimeout(timeoutId)
        if (error instanceof DOMException && error.name === 'AbortError') {
            throw new Error('请求超时，请重试（建议检查网络连接）')
        }
        throw error
    }
}

export function downloadXmind(num: number): Promise<{ blob: Blob; filename: string }> {
    return downloadFile(`/file/generateXmind?num=${num}`, `outline_${num}.xmind`)
}

export function downloadCsv(num: number): Promise<{ blob: Blob; filename: string }> {
    return downloadFile(`/file/generateCsv?num=${num}`, `testcases_${num}.csv`)
}
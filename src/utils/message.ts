type MessageType = 'success' | 'error' | 'warning' | 'info'

interface MessageOptions {
    duration?: number
    type?: MessageType
}

const colors: Record<MessageType, string> = {
    success: '#10b981',
    error: '#ef4444',
    warning: '#f59e0b',
    info: '#3b82f6',
}

const createMessageEl = (text: string, options: MessageOptions = {}): void => {
    const { duration = 3000, type = 'info' } = options

    const el = document.createElement('div')
    el.textContent = text
    el.style.cssText = `
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 24px;
    background: ${colors[type]};
    color: #fff;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    z-index: 10000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: opacity 0.3s, transform 0.3s;
    opacity: 0;
    transform: translateX(-50%) translateY(-10px);
    pointer-events: none;
  `

    document.body.appendChild(el)

    requestAnimationFrame(() => {
        el.style.opacity = '1'
        el.style.transform = 'translateX(-50%) translateY(0)'
    })

    setTimeout(() => {
        el.style.opacity = '0'
        el.style.transform = 'translateX(-50%) translateY(-10px)'
        setTimeout(() => el.remove(), 300)
    }, duration)
}

export const message = {
    success: (text: string, duration?: number) =>
        createMessageEl(text, { type: 'success', duration }),
    error: (text: string, duration?: number) =>
        createMessageEl(text, { type: 'error', duration }),
    warning: (text: string, duration?: number) =>
        createMessageEl(text, { type: 'warning', duration }),
    info: (text: string, duration?: number) =>
        createMessageEl(text, { type: 'info', duration }),
}

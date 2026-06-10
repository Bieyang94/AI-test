D:\project\AI-test\Dockerfile
# ---- 构建阶段 ----
FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache-dir -r pyproject.toml

# ---- 运行阶段 ----
FROM python:3.12-slim

# PyMuPDF / pdfplumber 等可能需要的系统库
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 从 builder 阶段拷贝已安装的 Python 依赖
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

# 拷贝项目代码
COPY app/ ./app/
COPY .env.example .env.example

# 运行时目录（通过 volume 挂载持久化）
RUN mkdir -p /app/app/service/server/upload_files \
             /app/app/service/server/cache \
             /app/app/service/server/debug_output

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.service.server.main:app", "--host", "0.0.0.0", "--port", "8000"]

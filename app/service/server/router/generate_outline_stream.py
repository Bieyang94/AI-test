import logging
import json

from fastapi import Query, APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.core.interface.agent_output import agent_output_markdown
from app.service.server.cache.docx_cache import get_cached_file
from app.service.server.cache.outLine_cache import set_cached_outline
from app.service.server.cache import clear_all_caches

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/file", tags=["输出大纲模块"])


def _sse_format(event: str, data: str) -> str:
    return f"event: {event}\ndata: {data}\n\n"


async def _collect_and_cache_sse(generator, num: int):
    full_text = ""
    chunk_index = 0

    try:
        async for chunk in generator:
            full_text += chunk
            payload = json.dumps({"index": chunk_index, "content": chunk}, ensure_ascii=False)
            yield _sse_format("chunk", payload)
            chunk_index += 1
    except Exception as e:
        logger.error("大纲生成流中断: %s", e)
        error_payload = json.dumps({"error": str(e)}, ensure_ascii=False)
        yield _sse_format("error", error_payload)
        return

    set_cached_outline(num, full_text)
    logger.info("大纲已缓存: num=%d, 长度=%d", num, len(full_text))

    done_payload = json.dumps({
        "status": "done",
        "num": num,
        "total_length": len(full_text),
    }, ensure_ascii=False)
    yield _sse_format("done", done_payload)


@router.post("/generateOutline", status_code=201, summary="基于已缓存文件流式输出大纲（SSE）")
async def generate_outline(
    num: int = Query(..., description="数字编号，对应已缓存文件的编号", ge=1),
):
    cached = get_cached_file(num)
    if not cached:
        raise HTTPException(
            status_code=404,
            detail=f"未找到编号 {num} 的缓存文件，请先调用 /file/upload 上传",
        )

    raw_text, ext = cached["raw_text"], cached["ext"]
    logger.info("生成大纲: num=%d, 类型=%s, 文本长度=%d", num, ext, len(raw_text))

    agent = agent_output_markdown(raw_text)
    return StreamingResponse(
        _collect_and_cache_sse(agent.agenerate_title_stream(), num),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.delete("/cache/{num}", status_code=200, summary="清除指定编号的所有缓存")
async def clear_cache(num: int):
    deleted = clear_all_caches(num)
    if deleted:
        return {"message": f"编号 {num} 的缓存已清除: {', '.join(deleted)}"}
    raise HTTPException(status_code=404, detail=f"编号 {num} 不存在任何缓存")

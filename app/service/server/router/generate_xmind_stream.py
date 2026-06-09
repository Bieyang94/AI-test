import logging

from fastapi import Query, APIRouter, HTTPException
from fastapi.responses import Response

from app.core.interface.agent_output import agent_output_markdown
from app.service.server.cache.outLine_cache import get_cached_outline
from app.service.server.cache.xmind_cache import set_cached_xmind, get_cached_xmind

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/file", tags=["XMind生成模块"])


@router.post("/generateXmind", status_code=201, summary="基于已缓存大纲生成 XMind 文件")
async def generate_xmind(
    num: int = Query(..., description="数字编号，对应已缓存大纲的编号", ge=1),
):
    outline = get_cached_outline(num)
    if not outline:
        raise HTTPException(
            status_code=404,
            detail=f"未找到编号 {num} 的大纲缓存，请先调用 /file/generateOutline 生成大纲",
        )

    logger.info("生成XMind: num=%d, 大纲长度=%d", num, len(outline))

    try:
        agent = agent_output_markdown(outline)
        result = await agent.generate_xmind(outline)

        if not result["xmind_bytes"]:
            raise HTTPException(status_code=500, detail="XMind 二进制生成失败")

        set_cached_xmind(num, result["xmind_bytes"], result["test_points"])
        logger.info("XMind已缓存: num=%d", num)

        return Response(
            content=result["xmind_bytes"],
            status_code=201,
            media_type="application/xmind",
            headers={"Content-Disposition": f"attachment; filename=outline_{num}.xmind"},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("XMind 生成失败")
        raise HTTPException(status_code=500, detail=f"XMind 生成失败：{str(e)}")


@router.post("/getXmindTestPoints", status_code=200, summary="获取已缓存的功能点文本")
async def get_xmind_test_points(
    num: int = Query(..., description="数字编号", ge=1),
):
    cached = get_cached_xmind(num)
    if not cached:
        raise HTTPException(
            status_code=404,
            detail=f"未找到编号 {num} 的 XMind 缓存，请先调用 /file/generateXmind 生成",
        )
    return {"num": num, "test_points": cached["test_points"]}

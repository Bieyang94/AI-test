import logging

from fastapi import Query, APIRouter, HTTPException
from fastapi.responses import Response

from app.core.interface.agent_output import agent_output_markdown
from app.service.server.cache.xmind_cache import get_cached_xmind
from app.service.server.cache.csv_cache import set_cached_csv, get_cached_csv

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/file", tags=["CSV生成模块"])


@router.post("/generateCsv", status_code=201, summary="基于已缓存功能点生成 CSV 测试用例")
async def generate_csv(
    num: int = Query(..., description="数字编号，对应已缓存 XMind 功能点的编号", ge=1),
):
    cached = get_cached_xmind(num)
    if not cached:
        raise HTTPException(
            status_code=404,
            detail=f"未找到编号 {num} 的功能点缓存，请先调用 /file/generateXmind 生成",
        )

    test_points = cached["test_points"]
    logger.info("生成CSV: num=%d, 功能点长度=%d", num, len(test_points))

    try:
        agent = agent_output_markdown("")
        csv_str = agent.generate_csv(test_points)

        if not csv_str:
            raise HTTPException(status_code=500, detail="CSV 生成结果为空")

        set_cached_csv(num, csv_str)
        logger.info("CSV已缓存: num=%d, 长度=%d", num, len(csv_str))

        return Response(
            content=csv_str.encode("utf-8-sig"),
            status_code=201,
            media_type="text/csv; charset=utf-8-sig",
            headers={"Content-Disposition": f"attachment; filename=testcases_{num}.csv"},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("CSV 生成失败")
        raise HTTPException(status_code=500, detail=f"CSV 生成失败：{str(e)}")


@router.post("/getCsv", status_code=200, summary="获取已缓存的 CSV 文件")
async def get_csv(
    num: int = Query(..., description="数字编号", ge=1),
):
    csv_content = get_cached_csv(num)
    if not csv_content:
        raise HTTPException(
            status_code=404,
            detail=f"未找到编号 {num} 的 CSV 缓存，请先调用 /file/generateCsv 生成",
        )

    return Response(
        content=csv_content.encode("utf-8-sig"),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename=testcases_{num}.csv"},
    )

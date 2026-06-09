from fastapi import UploadFile, File, APIRouter, HTTPException

from app.service.server.cache.docx_cache import (
    validate_file,
    read_file_to_text,
    set_cached_file,
)
from app.service.server.cache.num_counter import next_num

router = APIRouter(prefix="/file", tags=["文件上传模块"])


@router.post("/upload", status_code=201, summary="上传文件到内存缓存（支持 md / docx / pdf）")
async def upload_file(
    file: UploadFile = File(..., description="支持 .md / .docx / .pdf 格式文件"),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    try:
        ext = validate_file(file.filename)
        raw_text = await read_file_to_text(file, ext)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    num = next_num()
    set_cached_file(num, ext, raw_text)

    return {
        "num": num,
        "ext": ext,
        "text_length": len(raw_text),
        "message": f"文件已缓存到内存（编号 {num}），可调用 /file/generateOutline?num={num} 生成大纲",
    }

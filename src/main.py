from fastapi import FastAPI, UploadFile, HTTPException, status, Query
from fastapi_pagination import Page, add_pagination, paginate
from fastapi.responses import JSONResponse

from typing import Literal, Annotated

import aiofiles
import aiofiles.ospath
import aiofiles.os

import re

from .utils import (
    filter_by_username,
    process_result,
    run_script,
    store_file,
    validate_file_content,
    verify_or_create_store_folder
)
from .settings import settings

app = FastAPI()


@app.put('/')
async def upload_file(file: UploadFile):
    filename = file.filename
    
    if not re.fullmatch(settings.files.FILENAME_PATTERN, filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=settings.error_msg.FILENAME_NOT_VALID)
    
    file_content = await file.read()
    is_valid_data = await validate_file_content(file_content.decode())

    if not is_valid_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=settings.error_msg.INVALID_FILE_CONTENT)
    
    await verify_or_create_store_folder()
    is_overwriteen = await store_file(filename, file_content)
    
    if is_overwriteen:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=settings.response_msg.FILE_OVERWRITEEN)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=settings.response_msg.FILE_STORED)

@app.get('/')
async def list_files() -> Page[str]:
    files = await aiofiles.os.listdir(settings.path.FILE_STORE)
    return paginate(files)

@app.get('/users/')
async def get_users(
        filename: str, 
        user_size: Literal['min', 'max'] = None, 
        order: Literal['asc', 'desc'] = 'asc', 
        username: str = None, 
        inbox_range: Annotated[str | None, Query(pattern=r'\d+-\d+')] = None) -> Page[dict]:
    data_path = f'{settings.path.FILE_STORE}/{filename}'

    if not (await aiofiles.ospath.exists(data_path)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=settings.error_msg.FILE_NOT_EXISTS)
    
    scripts_pipeline = []
    result = []

    if order:
        scripts_pipeline.append({
            'name': 'order-by-user-name',
            'args': [f'-{order}']
        })

    if inbox_range:
        msg_min, msg_max = list(map(int, inbox_range.split('-')))

        if msg_min > msg_max:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=settings.error_msg.BAD_RANGE)

        scripts_pipeline.append({
            'name': 'between-msgs',
            'args': [msg_min, msg_max]
        })

    if user_size:
        scripts_pipeline.append({
            'name': 'max-min-size',
            'args': [f'-{user_size}']
        })

    for script in scripts_pipeline:
        result = await run_script(script, data_path)
        result = result.strip().split('\n')

    if username is not None:
        result = filter_by_username(result, username)

    return paginate(process_result(result))

add_pagination(app)

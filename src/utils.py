import aiofiles.os
import aiofiles.ospath
from fastapi import UploadFile, HTTPException, status
from typing import List
import asyncio
import aiofiles

from .settings import settings


async def run_script(script: dict, data_path: str):
    script_name, args = script.values()
    process = await asyncio.subprocess.create_subprocess_exec(
        f"{settings.path.SCRIPTS}/{script_name}.sh", data_path, *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise Exception(f"Shell script error: {stderr.decode()}")

    return stdout.decode()

def filter_by_username(results: List[str], username: str):
    return list(filter(lambda line: username in line.split()[0], results))

def process_result(result: List[str]) -> dict:
    def str_to_obj(item_str: str) -> dict:
        username, folder, msg_qtd, _, size = item_str.split()
        return {
            'username': username,
            'folder': folder,
            'numberMessages': msg_qtd,
            'size': size
        }
    
    return list(map(lambda item: str_to_obj(item), result))

async def store_file(filename: str, file_content: str):
    overwriteen = False
    path_to_store = f"{settings.path.FILE_STORE}/{filename}"

    if await aiofiles.ospath.exists(path_to_store):
        overwriteen = True

    async with aiofiles.open(path_to_store, 'wb+') as out_file:
        await out_file.write(file_content)

    return overwriteen

async def validate_file_content(file_content: str):
    def validate_line(line: str):
        return len(line.split()) == 5

    lines = file_content.split('\n')
    is_valid_data = False not in list(map(validate_line, lines))

    return is_valid_data

async def verify_or_create_store_folder():
    folder_exists = await aiofiles.ospath.isdir(settings.path.FILE_STORE)

    if not folder_exists:
        await aiofiles.os.mkdir(settings.path.FILE_STORE)
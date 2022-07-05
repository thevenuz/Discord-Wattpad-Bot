import json
from typing import Awaitable
import aiofiles
import logging
import os

errors={
    "EmptyFile":"file parameter cannot be empty."}


logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger(name="msghelper")
logger.setLevel(logging.ERROR)


async def read_from_json(file:str)->dict:
    """
        asynchronously read from a json file
    """
    try:
        logger.info("helpers.json_helper.read_from_json invoked for file:%s", file)

        filePath=await get_file_path(file)

         #async impl of reading json files
        async with aiofiles.open(filePath, mode="r") as f:
            result=json.loads(await f.read())

        return result

    except Exception as e:
        logger.fatal("Exception occured in helpers.json_helper.read_from_json invoked for file:%s", file, exc_info=1)
        raise e


async def write_to_json(file:str,data:dict)->bool:
    """
        asynchronously write to a json file
    """
    try:
        logger.info("helpers.json_helper.write_to_json invoked for file:%s", file)

        filePath=await get_file_path(file)

        #async impl of writing to json files
        async with aiofiles.open(filePath,mode="w") as f:
            await f.write(json.dumps(data,indent=2))

        return True

    except Exception as e:
        logger.fatal("Exception occured in helpers.json_helper.write_to_json invoked for file:%s", file, exc_info=1)
        raise e



async def get_file_path(file:str)->str:
        """
        Returns absolute file path.
        """
        try:
            logger.info("helpers.json_helper.get_file_path method invoked for file: %s",file)
            if file is None:
                raise TypeError(errors["EmptyFile"])
            
            filePath=os.path.join(os.path.dirname(os.path.dirname(__file__)), file)
            
            return filePath

        except Exception as e:
            logger.fatal("Exception occured in helpers.json_helper.get_file_path method for file: %s",file, exc_info=1)
            raise e
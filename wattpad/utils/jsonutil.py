from wattpad.logger.baselogger import BaseLogger
from typing import Dict
import os
import aiofiles
import json
from pathlib import Path


class JsonUtil:
    def __init__(self) -> None:
        self.filePrefix = "wattpad.utils.jsonutil"
        self.logger = BaseLogger().loggger_init()

    async def get_file_path(self, folder: str, file: str) -> str:
        """
            returns absolute file path
        """
        try:
            self.logger.info("%s.get_file_path method invoked for file: %s", self.filePrefix, file)

            if file is None:
                raise TypeError("empty file")

            rootDirectory=os.path.dirname(__file__)
            configDirectory=Path(rootDirectory).parents[1]

            filePath = os.path.join(configDirectory, folder, file)

            return filePath

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_file_path method for file: %s", self.filePrefix, file, exc_info=1)
            raise e

    async def read_from_json(self, folder: str, file: str) -> Dict:
        """
            read json data from a given json file in config folder
        """
        try:
            self.logger.info("%s.read_from_json method invoked for file: %s", self.filePrefix, file)

            filePath = await self.get_file_path(folder, file)

            async with aiofiles.open(filePath, mode="r") as f:
                result = json.loads(await f.read())

            return result

        except Exception as e:
            self.logger.info("Exception occured in %s.read_from_json for file: %s", self.filePrefix, file, exc_info=1)
            raise e
    
    async def write_to_json(self, folder: str, file: str, data: Dict) -> Dict:
        """
            writes json data to json file
        """
        try:
            self.logger.info("%s.write_to_json method invoked for file: %s", self.filePrefix, file)

            filePath = await self.get_file_path(folder, file)

            async with aiofiles.open(filePath, mode="w") as f:
                await f.write(json.dumps(data, indent=2))

            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.write_to_json method for file: %s", self.filePrefix, file, exc_info=1)
            raise e
        

import lightbulb
import hikari
from lightbulb.ext import tasks
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsimpl.tasks.taskimpl import TaskImpl

plugin = lightbulb.Plugin("TaskPlugin")

filePrefix = "wattpad.plugins.tasks.task"
logger = BaseLogger().loggger_init()


@tasks.task(m=10, auto_start=True, max_consecutive_failures=100)
async def get_new_chapters() -> None:
    try:
        logger.info("%s.get_new_chapters method invoked", filePrefix)

        #call the exec
        result= await TaskImpl().get_new_chapters(plugin)

        logger.info("get_new_chapters task ended")
    
    except Exception as e:
        logger.fatal("Exception occured in %s.get_new_chapters method", filePrefix, exc_info=1)
        raise e
    
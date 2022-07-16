import lightbulb
import hikari
from lightbulb.ext import tasks
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsexecution.tasksexecution.taskexec import TaskExec

plugin= lightbulb.Plugin("TaskPlugin")

file_prefix="wattpad.plugins.tasks.task"
logger=BaseLogger().loggger_init()

@tasks.task(m=10, auto_start=True, max_consecutive_failures=100)
async def get_new_chapters() -> None:
    try:
        logger.info("%s.get_new_chapters method invoked", file_prefix)

        #call the exec
        result= await TaskExec().get_new_chapters(plugin)

        logger.info("get_new_chapters task ended")
    
    except Exception as e:
        logger.fatal("Exception occured in %s.get_new_chapters method", file_prefix, exc_info=1)
        pass
    

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
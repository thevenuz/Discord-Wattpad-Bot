import lightbulb
import hikari
from lightbulb.ext import tasks
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsimpl.tasks.taskimpl import TaskImpl

plugin = lightbulb.Plugin("TaskPlugin", include_datastore=True)

filePrefix = "wattpad.plugins.tasks.task"
logger = BaseLogger().loggger_init()


@tasks.task(m=5, auto_start=True, max_consecutive_failures=1000)
async def get_new_chapters() -> None:
    try:
        logger.info("%s.get_new_chapters method invoked", filePrefix)

        # call the impl
        result = await TaskImpl().get_new_chapters(plugin)

        if not result:
            logger.fatal("Some error occured in %s.get_new_chapters", filePrefix)

        logger.info("%s.get_new_chapters task ended", filePrefix)

    except Exception as e:
        logger.fatal(
            "Exception occured in %s.get_new_chapters method", filePrefix, exc_info=1
        )
        raise e


@tasks.task(m=5, auto_start=True, max_consecutive_failures=1000)
async def get_new_announcements() -> None:
    try:
        logger.info("%s.get_new_announcements method invoked", filePrefix)

        # call the impl
        result = await TaskImpl().get_new_announcements(plugin)

        if not result:
            logger.fatal("Some error occured in %s.get_new_announcements", filePrefix)

        logger.info("get_new_announcements task ended")

    except Exception as e:
        logger.fatal(
            "Exception occured in %s.get_new_announcements method",
            filePrefix,
            exc_info=1,
        )


@tasks.task(d=5, auto_start=True, max_consecutive_failures=1000)
async def cleanup_stored_data() -> None:
    """Used for removing servers data from authors.json and stories.json if the bot's not present in the server."""

    try:
        logger.info("%s.cleanup_stored_data method invoked", filePrefix)

        # call the impl
        result = await TaskImpl().cleanup_stored_data(plugin)

        if not result:
            logger.fatal("Some error occured in %s.cleanup_stored_data", filePrefix)

        logger.info("%s.cleanup_stored_data task ended", filePrefix)

    except Exception as e:
        logger.fatal(
            "Exception occured in %s.cleanup_stored_data method",
            filePrefix,
            exc_info=1,
        )


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)

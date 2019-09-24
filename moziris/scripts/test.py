import logging

from moziris.api import Location
from moziris.api.mouse.mouse import hover

logger = logging.getLogger(__name__)


def api_test():
    logger.error("Move mouse to 100, 100")
    hover(Location(100, 100))

    logger.error("Move mouse to 400, 100")
    hover(Location(400, 100))

    logger.error("Move mouse to 400, 400")
    hover(Location(400, 400))

    logger.error("Move mouse to 100, 400")
    hover(Location(100, 400))

    logger.error("Move mouse to 100, 100")
    hover(Location(100, 100))

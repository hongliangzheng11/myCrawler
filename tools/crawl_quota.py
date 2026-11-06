"""Process-wide quota for persisted crawler content."""

import asyncio

import config
from tools import utils


class ContentQuota:
    """Reserve content slots so every storage backend shares one total limit."""

    def __init__(self) -> None:
        self._count = 0
        self._lock = asyncio.Lock()
        self._limit_reported = False

    async def reserve(self) -> bool:
        limit = config.CRAWLER_TOTAL_MAX_NOTES_COUNT
        if limit is None:
            return True

        async with self._lock:
            if self._count >= limit:
                if not self._limit_reported:
                    utils.logger.info(
                        "[ContentQuota] Global content limit of %s reached; "
                        "additional items will not be saved.",
                        limit,
                    )
                    self._limit_reported = True
                return False

            self._count += 1
            return True


content_quota = ContentQuota()

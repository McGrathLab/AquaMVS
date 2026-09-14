"""CUDA caching-allocator configuration."""

import logging
import os
import sys

logger = logging.getLogger(__name__)

ALLOC_CONF_VAR = "PYTORCH_CUDA_ALLOC_CONF"


def configure_cuda_allocator() -> None:
    """Enable expandable segments in PyTorch's CUDA caching allocator.

    Dense matching makes multi-GiB allocations late in a run. With the default
    allocator, reserved-but-unallocated blocks left behind by earlier work can
    fragment the pool badly enough that such a request fails even when total
    free memory exceeds its size (e.g. RoMa full mode requesting 3.59 GiB with
    3.61 GiB free). Expandable segments let the allocator grow existing
    segments instead, which avoids these OOMs.

    PyTorch reads this setting when the allocator initializes, so this must be
    called before the first CUDA allocation; importing torch beforehand is
    fine. Calling it afterwards has no effect.

    The environment is left untouched if the user has already set
    ``expandable_segments`` either way, and on Windows, where PyTorch does not
    support it.
    """
    if sys.platform == "win32":
        return

    alloc_conf = os.environ.get(ALLOC_CONF_VAR, "")
    if "expandable_segments" in alloc_conf:
        return

    os.environ[ALLOC_CONF_VAR] = f"{alloc_conf},expandable_segments:True".lstrip(",")
    logger.debug("Set %s=%s", ALLOC_CONF_VAR, os.environ[ALLOC_CONF_VAR])

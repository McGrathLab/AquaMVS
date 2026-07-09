"""Shared pytest fixtures for AquaMVS tests."""

import os
import urllib.error

# Must be set before Open3D is imported to prevent segfault on headless CI
os.environ.setdefault("OPEN3D_CPU_RENDERING", "true")

import pytest
import torch


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Skip (rather than fail) tests on *transient* model-weight download errors.

    Feature extractors and matchers (SuperPoint, ALIKED, DISK via LightGlue,
    RoMa) fetch pretrained weights over the network on first use. A transient
    CDN outage would otherwise fail the release test gate, so convert transient
    network errors raised during the test call into a skip.

    Only transient failures are skipped: HTTP 5xx (server/gateway, e.g. 504) and
    connection-level errors (timeout, DNS, refused). A 4xx HTTPError (e.g. 404 or
    403) means the weights URL is wrong or removed -- a real defect that must
    fail loudly rather than be silently skipped.
    """
    outcome = yield
    excinfo = outcome.excinfo
    if excinfo is None:
        return
    exc = excinfo[1]
    if isinstance(exc, urllib.error.HTTPError):
        transient = exc.code >= 500
    elif isinstance(exc, urllib.error.URLError):
        transient = True  # connection-level failure (no HTTP status)
    else:
        transient = False
    if transient:
        outcome.force_exception(
            pytest.skip.Exception(
                f"Transient network failure downloading model weights ({exc}); "
                "skipping network-dependent test."
            )
        )


@pytest.fixture(params=["cpu", "cuda"])
def device(request):
    """Parametrized device fixture for CPU and CUDA testing.

    Args:
        request: pytest fixture request object.

    Returns:
        torch.device: Device to use for testing.

    Raises:
        pytest.skip: If CUDA is requested but not available.
    """
    if request.param == "cuda" and not torch.cuda.is_available():
        pytest.skip("CUDA not available")
    return torch.device(request.param)

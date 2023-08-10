from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import responses

from content_lint.types import Settings

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        supported_code_templates_languages={
            'python3',
            'java',
            'javascript',
            'go',
            'java17',
        }
    )


@pytest.fixture(autouse=True)
def rsps() -> Generator[responses.RequestsMock, None, None]:
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps

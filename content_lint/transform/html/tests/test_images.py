from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest
import responses
from bs4 import BeautifulSoup
from PIL.Image import Image
from requests import HTTPError, RequestException, Timeout
from transform.html.images import prepare_images


@pytest.fixture()
def mock_image() -> bytes:
    in_memory_image_file = BytesIO()
    image = Image.new('RGB', size=(640, 480), color=(155, 0, 0))
    image.save(in_memory_image_file, 'jpeg')
    in_memory_image_file.name = 'test.jpeg'
    in_memory_image_file.seek(0)
    return in_memory_image_file.getvalue()


@pytest.fixture()
def mock_image_url() -> str:
    return 'http://example.com/image.png'


@pytest.fixture()
def _mock_successful_image_response(
    rsps: responses.RequestsMock,
    mock_image_url: str,
    mock_image: bytes,
) -> None:
    rsps.add(responses.GET, mock_image_url, body=mock_image)


@pytest.fixture()
def _mock_successful_px_vector_image_response(
    rsps: responses.RequestsMock,
    mock_image_url: str,
) -> None:
    """Return image generated with Figma."""
    svg_bytes = (Path(__file__).parent / 'resources' / 'drawing_px.svg').read_bytes()
    rsps.add(responses.GET, mock_image_url, body=svg_bytes)


@pytest.fixture()
def _mock_successful_mm_vector_image_response(
    rsps: responses.RequestsMock,
    mock_image_url: str,
) -> None:
    """Return image generated with Inkscape. Width and height in mm."""
    svg_bytes = (Path(__file__).parent / 'resources' / 'drawing_mm.svg').read_bytes()
    rsps.add(responses.GET, mock_image_url, body=svg_bytes)


@pytest.fixture()
def _mock_successful_ex_vector_image_response(
    rsps: responses.RequestsMock,
    mock_image_url: str,
) -> None:
    """Return svg image with width and height in ex."""
    svg_bytes = (Path(__file__).parent / 'resources' / 'drawing_ex.svg').read_bytes()
    rsps.add(responses.GET, mock_image_url, body=svg_bytes)


@pytest.fixture()
def _mock_not_found_image_response(
    rsps: responses.RequestsMock,
    mock_image_url: str,
) -> None:
    rsps.add(responses.GET, mock_image_url, status=404)


@pytest.fixture()
def _mock_timeout_image_response(
    rsps: responses.RequestsMock,
    mock_image_url: str,
) -> None:
    rsps.add(responses.GET, mock_image_url, body=Timeout())


@pytest.mark.usefixtures(
    '_mock_successful_image_response',
)
def test_prepare_img(rsps: responses.RequestsMock, mock_image_url: str) -> None:
    text = f'<img name="something.jpeg" src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        'alt="" '
        'height="480" '
        'name="something.jpeg" '
        f'src="{mock_image_url}" '
        'width="640"'
        '/>'
        '</body></html>'
    )


def test_prepare_img_if_there_style_copy_value_from_it(
    rsps: responses.RequestsMock, mock_image_url: str
) -> None:
    text = (
        f'<img name="something.jpeg" style="width:10px;height:50px" '
        f'src="{mock_image_url}"/>'
    )
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        'alt="" '
        'height="50" '
        'name="something.jpeg" '
        f'src="{mock_image_url}" '
        'width="10"'
        '/>'
        '</body></html>'
    )


def test_prepare_img_dont_change_alt_height_and_width(mock_image_url: str) -> None:
    alt_text = 'something'
    width, height = 800, 600
    text = (
        f'<img alt="{alt_text}" width="{width}" '
        f'height="{height}" src="{mock_image_url}"/>'
    )
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        f'alt="{alt_text}" height="{height}" '
        f'src="{mock_image_url}" '
        f'width="{width}"'
        '/>'
        '</body></html>'
    )


def test_prepare_img_change_height_and_width_to_value_without_px(
    mock_image_url: str,
) -> None:
    alt_text = 'something'
    width, height = 800, 600
    text = (
        f'<img alt="{alt_text}" width="{width}px" '
        f'height="{height}px" src="{mock_image_url}"/>'
    )
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        f'alt="{alt_text}" height="{height}" '
        f'src="{mock_image_url}" '
        f'width="{width}"'
        '/>'
        '</body></html>'
    )


@pytest.mark.usefixtures('_mock_successful_image_response')
@pytest.mark.parametrize(
    'tag_image_dimensions',
    [
        'width="auto" height="auto"',
        'height="auto"',
        'width="auto"',
        'width="10%" height="30%"',
    ],
)
def test_prepare_img_remove_non_px_and_set_value_from_image(
    mock_image_url: str, tag_image_dimensions: str
) -> None:
    alt_text = 'something'
    text = f'<img alt="{alt_text}" width="auto" height="auto" src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        f'alt="{alt_text}" height="480" '
        f'src="{mock_image_url}" '
        'width="640"'
        '/>'
        '</body></html>'
    )


@pytest.mark.usefixtures('_mock_successful_px_vector_image_response')
@pytest.mark.parametrize(
    'tag_image_dimensions',
    [
        'width="auto" height="auto"',
        'height="auto"',
        'width="auto"',
        'width="10%" height="30%"',
    ],
)
def test_prepare_img_remove_non_px_and_set_value_from_vector_image(
    mock_image_url: str, tag_image_dimensions: str
) -> None:
    alt_text = 'something'
    text = f'<img alt="{alt_text}" width="auto" height="auto" src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        f'alt="{alt_text}" height="100" '
        f'src="{mock_image_url}" '
        'width="200"'
        '/>'
        '</body></html>'
    )


@pytest.mark.usefixtures('_mock_successful_mm_vector_image_response')
@pytest.mark.parametrize(
    'tag_image_dimensions',
    [
        'width="auto" height="auto"',
        'height="auto"',
        'width="auto"',
        'width="10%" height="30%"',
    ],
)
def test_prepare_img_remove_non_mm_and_set_value_from_vector_image(
    mock_image_url: str, tag_image_dimensions: str
) -> None:
    alt_text = 'something'
    text = f'<img alt="{alt_text}" width="auto" height="auto" src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        f'alt="{alt_text}" height="1123" '
        f'src="{mock_image_url}" '
        'width="794"'
        '/>'
        '</body></html>'
    )


@pytest.mark.usefixtures(
    '_mock_not_found_image_response',
)
def test_prepare_img_dont_change_if_there_is_404_error(
    rsps: responses.RequestsMock, mock_image_url: str
) -> None:
    text = f'<img src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    with pytest.raises(HTTPError):
        prepare_images(bs)

    assert str(bs) == f'<html><body><img alt="" src="{mock_image_url}"/></body></html>'


@pytest.mark.usefixtures('_mock_timeout_image_response')
def test_prepare_img_dont_change_if_there_is_timeout_error(
    rsps: responses.RequestsMock, mock_image_url: str
) -> None:
    text = f'<img src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    with pytest.raises(RequestException):
        prepare_images(bs)

    assert str(bs) == f'<html><body><img alt="" src="{mock_image_url}"/></body></html>'


@pytest.mark.usefixtures('_mock_successful_image_response')
@pytest.mark.parametrize(
    ('size_attr', 'width_value', 'height_value'),
    [
        ('width="20"', 20, 15),
        ('width="2000"', 2000, 1500),
        ('width="7"', 7, 6),
        ('width="8"', 8, 6),
        ('style="width:20px"', 20, 15),
        ('width="10" style="width:20px"', 20, 15),
        ('width="20" style="width:40px;height:50%"', 40, 30),
        ('width="20" height="790%"', 20, 15),
        ('width="0"', 0, 0),
        ('width="-100"', 640, 480),
    ],
)
def test_prepare_img_if_there_only_height_set_width_based_on_original_size(
    rsps: responses.RequestsMock,
    mock_image_url: str,
    size_attr: str,
    width_value: int,
    height_value: int,
) -> None:
    text = f'<img {size_attr} src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        f'alt="" height="{height_value}" '
        f'src="{mock_image_url}" '
        f'width="{width_value}"'
        '/>'
        '</body></html>'
    )


@pytest.mark.usefixtures('_mock_successful_image_response')
@pytest.mark.parametrize(
    'size_attr',
    [
        'height="20"',
        'height="2000"',
        'height="7px"',
        'height="8%"',
        'style="height:20px"',
        'height="100" width="100" style="height:20px"',
        'width="-100" height="auto"',
    ],
)
def test_prepare_img_if_there_only_width_set_height_and_width_based_on_original_size(
    rsps: responses.RequestsMock,
    mock_image_url: str,
    size_attr: str,
) -> None:
    text = f'<img {size_attr} src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        f'alt="" height="480" '
        f'src="{mock_image_url}" '
        f'width="640"'
        '/>'
        '</body></html>'
    )


@pytest.mark.usefixtures(
    '_mock_successful_ex_vector_image_response',
)
def test_parse_svg_image_with_scale_in_ex_unit(mock_image_url: str) -> None:
    alt_text = 'something'
    text = f'<img alt="{alt_text}" width="auto" height="auto" src="{mock_image_url}"/>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == (
        '<html><body>'
        '<img '
        f'alt="{alt_text}" height="auto" '
        f'src="{mock_image_url}" '
        'width="auto"'
        '/>'
        '</body></html>'
    )


def test_prepare_empty_img() -> None:
    text = '<img/>'
    bs = BeautifulSoup(text, 'lxml')

    prepare_images(bs)

    assert str(bs) == '<html><body></body></html>'

from __future__ import annotations

import math
from io import BytesIO
from typing import TYPE_CHECKING

import cssutils
import requests
import structlog
from PIL import Image, UnidentifiedImageError
from svgelements import SVG

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

logger = structlog.getLogger()


def fetch_image_size(url: str) -> tuple[int | None, int | None]:
    image_response = requests.get(url, timeout=(1, 5))
    image_response.raise_for_status()
    try:
        return Image.open(BytesIO(image_response.content)).size
    except UnidentifiedImageError:
        # maybe image is vector than try to parse width and height from it
        try:
            svg_image = SVG.parse(BytesIO(image_response.content))
            return math.ceil(svg_image.width), math.ceil(svg_image.height)
        except Exception as exception:
            logger.exception(
                'SVG parse error',
                image_url=url,
                detail=str(exception),
            )
            return None, None


def pop_size_from_style(image: BeautifulSoup) -> tuple[int | None, int | None]:
    if image_style := image.get('style'):
        style = cssutils.parseStyle(image_style)
        width, height = style.removeProperty('width'), style.removeProperty('height')
        if css_text := style.cssText:
            image['style'] = css_text
        else:
            image.attrs.pop('style')
        return normalize_dimension(width), normalize_dimension(height)
    return None, None


def get_dimensions_from_attr(image: BeautifulSoup) -> tuple[int | None, int | None]:
    return (
        normalize_dimension(image.attrs.get('width')),
        normalize_dimension(image.attrs.get('height')),
    )


def normalize_dimension(dimension_value: str | int | None) -> int | None:
    if dimension_value is None:
        return None
    if str_value := str(dimension_value).rstrip('px').strip('auto'):
        try:
            value = int(str_value)
        except ValueError:
            return None
        if value >= 0:
            return value
    return None


def get_height_based_on_aspect_ratio(
    width: int, image_width: int, image_height: int
) -> int:
    return math.ceil(width * image_height / image_width)


def prepare_images(bs: BeautifulSoup) -> None:
    images = bs.find_all('img')
    for image in images:
        if 'src' not in image.attrs:
            image.extract()
            continue

        if 'alt' not in image.attrs:
            image['alt'] = ''
        # 1. pop from style
        width, height = pop_size_from_style(image)
        if width is None and height is None:
            # 2. if there's nothing in style pop from attribute
            width, height = get_dimensions_from_attr(image)

        if width is not None and height is None:
            # 3. if there's width but no height set image size based on aspect ratio
            image_width, image_height = fetch_image_size(image['src'])
            if image_width is not None and image_height is not None:
                height = get_height_based_on_aspect_ratio(
                    width, image_width, image_height
                )
        elif width is None:
            # 4. if there's no width than set image size based on original size
            width, height = fetch_image_size(image['src'])

        if width is not None:
            image['width'] = width
        if height is not None:
            image['height'] = height

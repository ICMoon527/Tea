from PIL import Image, ImageDraw

ICON_SIZE = 48
_icon_cache = {}


def _new_icon():
    return Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))


def _circle_center(draw, xy, r, **kwargs):
    draw.ellipse(xy, **kwargs)


def _get_color(primary=False):
    if primary:
        return (137, 180, 250)
    return (100, 100, 100)


def _draw_clipboard():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.rounded_rectangle((10, 6, 38, 42), radius=4, outline=c, width=2)
    d.line((18, 14, 18, 6), fill=c, width=2)
    d.line((30, 14, 30, 6), fill=c, width=2)
    d.rectangle((16, 18, 32, 22), fill=c)
    d.rectangle((16, 26, 32, 30), fill=c)
    d.rectangle((16, 34, 28, 38), fill=c)
    return img


def _draw_trash():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = (239, 68, 68)
    d.line((12, 12, 36, 12), fill=c, width=2)
    d.line((14, 12, 16, 42), fill=c, width=2)
    d.line((34, 12, 32, 42), fill=c, width=2)
    d.line((18, 42, 30, 42), fill=c, width=2)
    d.line((22, 12, 22, 8), fill=c, width=2)
    d.line((26, 12, 26, 8), fill=c, width=2)
    d.line((18, 20, 30, 20), fill=c, width=2)
    d.line((18, 28, 30, 28), fill=c, width=2)
    return img


def _draw_plus():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.ellipse((6, 6, 42, 42), outline=c, width=2)
    d.line((24, 14, 24, 34), fill=c, width=3)
    d.line((14, 24, 34, 24), fill=c, width=3)
    return img


def _draw_edit():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.line((14, 34, 14, 16), fill=c, width=2)
    d.line((14, 16, 24, 6), fill=c, width=2)
    d.line((24, 6, 38, 20), fill=c, width=2)
    d.line((38, 20, 28, 30), fill=c, width=2)
    d.line((28, 30, 16, 42), fill=c, width=2)
    d.line((16, 42, 14, 34), fill=c, width=2)
    d.polygon([(18, 22), (24, 16), (32, 24), (26, 30)], fill=c)
    return img


def _draw_download():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.rectangle((10, 34, 38, 42), outline=c, width=2)
    d.line((24, 8, 24, 30), fill=c, width=3)
    d.line((16, 22, 24, 32), fill=c, width=3)
    d.line((24, 32, 32, 22), fill=c, width=3)
    return img


def _draw_search():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.ellipse((8, 8, 32, 32), outline=c, width=2)
    d.line((28, 28, 40, 40), fill=c, width=3)
    return img


def _draw_box():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.rectangle((10, 16, 38, 40), outline=c, width=2)
    d.line((10, 16, 6, 10), fill=c, width=2)
    d.line((38, 16, 42, 10), fill=c, width=2)
    d.line((6, 10, 42, 10), fill=c, width=2)
    d.line((22, 16, 22, 22), fill=c, width=2)
    d.line((16, 22, 28, 22), fill=c, width=2)
    return img


def _draw_users():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.ellipse((18, 6, 30, 18), outline=c, width=2)
    d.ellipse((26, 24, 42, 40), outline=c, width=2)
    d.ellipse((6, 24, 22, 40), outline=c, width=2)
    return img


def _draw_calendar():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.rounded_rectangle((6, 10, 42, 42), radius=4, outline=c, width=2)
    d.rectangle((6, 10, 42, 22), fill=c)
    d.rectangle((10, 14, 16, 18), fill=(255, 255, 255))
    d.rectangle((20, 14, 26, 18), fill=(255, 255, 255))
    d.rectangle((14, 28, 20, 32), fill=c)
    d.rectangle((24, 28, 30, 32), fill=c)
    d.rectangle((14, 36, 18, 40), fill=c)
    return img


def _draw_cart():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.line((8, 16, 16, 36), fill=c, width=2)
    d.line((16, 36, 32, 36), fill=c, width=2)
    d.line((32, 36, 40, 16), fill=c, width=2)
    d.line((6, 16, 42, 16), fill=c, width=2)
    d.ellipse((10, 36, 18, 44), outline=c, width=2)
    d.ellipse((28, 36, 36, 44), outline=c, width=2)
    return img


def _draw_credit_card():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.rounded_rectangle((4, 12, 44, 34), radius=5, outline=c, width=2)
    d.rectangle((6, 18, 18, 26), fill=c)
    d.rectangle((26, 24, 38, 28), fill=c)
    return img


def _draw_chart_line():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.line((8, 38, 42, 38), fill=c, width=2)
    d.line((8, 38, 8, 6), fill=c, width=2)
    d.line((8, 28, 18, 18, 30, 24, 40, 10), fill=c, width=2)
    return img


def _draw_trophy():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = (255, 200, 0)
    d.line((18, 6, 30, 6), fill=c, width=2)
    d.line((14, 8, 16, 22), fill=c, width=2)
    d.line((34, 8, 32, 22), fill=c, width=2)
    d.arc((8, 10, 22, 26), start=210, end=330, fill=c, width=2)
    d.arc((26, 10, 40, 26), start=210, end=330, fill=c, width=2)
    d.rectangle((16, 22, 32, 30), fill=c)
    d.rectangle((10, 30, 38, 34), fill=c)
    return img


def _draw_dollar():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.ellipse((10, 6, 38, 34), outline=c, width=2)
    d.line((24, 2, 24, 40), fill=c, width=2)
    d.line((16, 16, 24, 24), fill=c, width=2)
    d.line((24, 24, 32, 16), fill=c, width=2)
    return img


def _draw_chart_bar():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.line((8, 38, 42, 38), fill=c, width=2)
    d.line((8, 6, 8, 38), fill=c, width=2)
    d.rectangle((12, 24, 20, 38), fill=c)
    d.rectangle((22, 12, 30, 38), fill=c)
    d.rectangle((32, 20, 40, 38), fill=c)
    return img


def _draw_save():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.rounded_rectangle((8, 6, 40, 42), radius=3, outline=c, width=2)
    d.rectangle((8, 6, 40, 16), fill=c)
    d.rectangle((14, 8, 20, 12), fill=(255, 255, 255))
    d.rectangle((32, 6, 40, 14), fill=c)
    d.rectangle((14, 20, 34, 28), outline=c, width=2)
    d.rectangle((14, 32, 34, 38), fill=c)
    return img


def _draw_cloud():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.ellipse((10, 20, 22, 32), fill=c)
    d.ellipse((18, 10, 34, 24), fill=c)
    d.ellipse((28, 18, 42, 30), fill=c)
    d.rectangle((10, 24, 42, 34), fill=c)
    return img


def _draw_file_text():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.rounded_rectangle((8, 6, 40, 42), radius=4, outline=c, width=2)
    d.polygon([(32, 6), (32, 14), (40, 14)], fill=c)
    d.line((32, 6, 32, 14), fill=c, width=2)
    d.line((32, 14, 40, 14), fill=c, width=2)
    d.rectangle((14, 20, 34, 24), fill=c)
    d.rectangle((14, 28, 30, 32), fill=c)
    d.rectangle((14, 36, 26, 40), fill=c)
    return img


def _draw_moon():
    img = _new_icon()
    d = ImageDraw.Draw(img)
    c = _get_color(True)
    d.ellipse((8, 6, 40, 38), outline=c, width=2)
    d.ellipse((18, 2, 48, 42), fill=(30, 30, 30))
    return img


_ICON_MAP = {
    "\U0001f4cb": _draw_clipboard,
    "\U0001f5d1\ufe0f": _draw_trash,
    "\U0001f5d1": _draw_trash,
    "\U00002795": _draw_plus,
    "\U0000270f\ufe0f": _draw_edit,
    "\U0000270f": _draw_edit,
    "\U0001f4e5": _draw_download,
    "\U0001f50d": _draw_search,
    "\U0001f50e": _draw_search,
    "\U0001f4e6": _draw_box,
    "\U0001f465": _draw_users,
    "\U0001f4c5": _draw_calendar,
    "\U0001f6d2": _draw_cart,
    "\U0001f4b3": _draw_credit_card,
    "\U0001f4c8": _draw_chart_line,
    "\U0001f3c6": _draw_trophy,
    "\U0001f4b0": _draw_dollar,
    "\U0001f4ca": _draw_chart_bar,
    "\U0001f4be": _draw_save,
    "\u2601\ufe0f": _draw_cloud,
    "\u2601": _draw_cloud,
    "\U0001f4dd": _draw_file_text,
    "\U0001f313": _draw_moon,
}


def get_icon(emoji, size=None):
    key = (emoji, size or ICON_SIZE)
    if key in _icon_cache:
        return _icon_cache[key]

    draw_func = _ICON_MAP.get(emoji)
    if draw_func is None:
        return None

    img = draw_func()
    if size and size != ICON_SIZE:
        img = img.resize((size, size), Image.LANCZOS)

    _icon_cache[key] = img
    return img


def get_icon_map():
    return _ICON_MAP
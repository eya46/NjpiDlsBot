import math
import os
from base64 import b64encode
from io import BytesIO

from nonebot.adapters.onebot.v11 import MessageSegment
from PIL import Image, ImageDraw, ImageFont
from wcwidth import wcwidth

local = os.path.dirname(__file__)
BACKGROUND_FILE = os.path.join(local, "data/image/background.png".replace("/", "\\"))
BANNER_FILE = os.path.join(local, "data/image/banner.png".replace("/", "\\"))
FONT_FILE = os.path.join(local, "data/font/qsz-lgy85.ttf".replace("/", "\\"))


class Txt2Img:
    """Share your text as a image"""

    def __init__(self, size=30):
        self.font_family = str(FONT_FILE)
        # self.save_dir = str(IMAGE_PATH)
        # self.out_img_name = "save.png"
        self.user_font_size = int(size * 1.5)
        self.lrc_font_size = int(size)
        self.line_space = int(size)
        self.lrc_line_space = int(size / 2)
        self.stroke = 5
        self.share_img_width = 1080

    def wrap(self, string):
        max_width = int(1850 / self.lrc_font_size)
        temp_len = 0
        result = ""
        for ch in string:
            result += ch
            temp_len += wcwidth(ch)
            if ch == "\n":
                temp_len = 0
            if temp_len >= max_width:
                temp_len = 0
                result += "\n"
        result = result.rstrip()
        return result

    def save(self, title, lrc):
        return self.img2b64(self.draw_pic(title, lrc))

    def draw_pic(self, title, lrc) -> Image:
        """MI Note"""
        border_color = (220, 211, 196)
        text_color = (125, 101, 89)

        out_padding = 30
        padding = 45
        banner_size = 20

        user_font = ImageFont.truetype(self.font_family, self.user_font_size)
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        if title == " ":
            title = ""

        lrc = self.wrap(lrc)

        if lrc.find("\n") > -1:
            lrc_rows = len(lrc.split("\n"))
        else:
            lrc_rows = 1

        w = self.share_img_width

        if title:
            inner_h = (
                padding * 2
                + self.user_font_size
                + self.line_space
                + self.lrc_font_size * lrc_rows
                + (lrc_rows - 1) * self.lrc_line_space
            )
        else:
            inner_h = padding * 2 + self.lrc_font_size * lrc_rows + (lrc_rows - 1) * (self.lrc_line_space)

        h = out_padding * 2 + inner_h

        out_img = Image.new(mode="RGB", size=(w, h), color=(255, 255, 255))
        draw = ImageDraw.Draw(out_img)

        mi_img = Image.open(BACKGROUND_FILE)
        mi_banner = Image.open(BANNER_FILE).resize((banner_size, banner_size), resample=3)

        # add background
        for x in range(int(math.ceil(h / 100))):
            out_img.paste(mi_img, (0, x * 100))

        # add border
        def draw_rectangle(draw, rect, width):
            for i in range(width):
                draw.rectangle(
                    (rect[0] + i, rect[1] + i, rect[2] - i, rect[3] - i),
                    outline=border_color,
                )

        draw_rectangle(draw, (out_padding, out_padding, w - out_padding, h - out_padding), 2)

        # add banner
        out_img.paste(mi_banner, (out_padding, out_padding))
        out_img.paste(
            mi_banner.transpose(Image.FLIP_TOP_BOTTOM),
            (out_padding, h - out_padding - banner_size + 1),
        )
        out_img.paste(
            mi_banner.transpose(Image.FLIP_LEFT_RIGHT),
            (w - out_padding - banner_size + 1, out_padding),
        )
        out_img.paste(
            mi_banner.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM),
            (w - out_padding - banner_size + 1, h - out_padding - banner_size + 1),
        )

        if title:
            user_w, user_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
                title, font=user_font, spacing=self.line_space
            )
            draw.text(
                ((w - user_w) // 2, out_padding + padding),
                title,
                font=user_font,
                fill=text_color,
                spacing=self.line_space,
            )
            draw.text(
                (
                    out_padding + padding,
                    out_padding + padding + self.user_font_size + self.line_space,
                ),
                lrc,
                font=lyric_font,
                fill=text_color,
                spacing=self.lrc_line_space,
            )
        else:
            draw.text(
                (out_padding + padding, out_padding + padding),
                lrc,
                font=lyric_font,
                fill=text_color,
                spacing=self.lrc_line_space,
            )
        return out_img

    def img2b64(self, out_img) -> str:
        """image to base64"""
        buf = BytesIO()
        out_img.save(buf, format="PNG")
        base64_str = "base64://" + b64encode(buf.getvalue()).decode()
        return base64_str


def to_pic(title, txt, size=30) -> MessageSegment:
    return MessageSegment.image(Txt2Img(size).save(title, txt))


def to_img(title, txt, size=30) -> Image:
    return Txt2Img(size).draw_pic(title, txt)

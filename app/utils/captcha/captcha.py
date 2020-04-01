import random
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

basedir = os.path.abspath(os.path.dirname(__file__))


class CaptchaUtils:
    def __init__(self):
        # 字体路径
        self.fonts = ['Ubuntu_regular.ttf', 'Open_Sans_regular.ttf', 'Roboto_regular.ttf', 'Lora-Regular.ttf']
        # 生成验证码位数
        self.text_num = 4
        # 生成图片尺寸
        self.pic_size = (120, 40)
        # 背景颜色，默认为白色
        self.bg_color = (255, 255, 255)
        # 字体颜色，默认为蓝色
        self.text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # 干扰线颜色，默认为红色
        self.line_color = (255, 0, 0)
        # 是否加入干扰线
        self.draw_line = False
        # 加入干扰线条数上下限
        self.line_number = (1, 5)
        # 是否加入干扰点
        self.draw_points = False
        # 干扰点出现的概率(%)
        self.point_chance = 5

        self.image = Image.new('RGB', (self.pic_size[0], self.pic_size[1]), self.bg_color)
        self.font = ImageFont.truetype(os.path.join(basedir, 'fonts/' + random.choice(self.fonts)),
                                       22)
        self.draw = ImageDraw.Draw(self.image)
        self.text = self.gene_text()

    def gene_text(self):
        # 5位随机数
        return str(random.randint(10 ** (self.text_num - 1), (10 ** self.text_num)))

    def gene_line(self):
        # 随机生成干扰线
        begin = (random.randint(0, self.pic_size[0]), random.randint(0, self.pic_size[1]))
        end = (random.randint(0, self.pic_size[0]), random.randint(0, self.pic_size[1]))
        self.draw.line([begin, end], fill=self.line_color)

    def gene_points(self):
        # 随机绘制干扰点
        for w in range(self.pic_size[0]):
            for h in range(self.pic_size[1]):
                tmp = random.randint(0, 100)
                if tmp > 100 - self.point_chance:
                    self.draw.point((w, h), fill=(0, 0, 0))

    def gen_code(self):
        # 生成验证码图片
        font_width, font_height = self.font.getsize(self.text)
        for ind in range(len(self.text)):
            self.draw.text(
                (10 + (ind * (self.pic_size[0] - 30) / self.text_num),
                 (self.pic_size[1] - font_height) / self.text_num),
                self.text[ind],
                font=self.font,
                fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        if self.draw_line:
            n = random.randint(self.line_number[0], self.line_number[1])
            for i in range(n):
                self.gene_line()
        if self.draw_points:
            self.gene_points()
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        self.image = self.image.transform((self.pic_size[0], self.pic_size[1]), Image.PERSPECTIVE,
                                          params)  # 创建扭曲
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 边界加强
        image_file = BytesIO()
        self.image.save(image_file, 'jpeg')
        return {'image_file': image_file, 'code': self.text}

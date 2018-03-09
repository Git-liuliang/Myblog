from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from io import BytesIO

def randomChar():
    return chr(random.randint(65,90))

def randomNum():
    return str(random.randint(0,9))

def random_font():

    return random.choices([randomChar(),randomNum()])


def randomcolor():
    return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

def get_valid(request):
    width = 200
    heigh = 50
    image = Image.new('RGB', (width, heigh), randomcolor())
    font = ImageFont.truetype('LBRITED.TTF', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    keep_valid_codes = ''
    for t in range(6):
        rand = random_font()[0]
        draw.text((30 * t + 5, 5), rand, font=font, fill=randomcolor())
        keep_valid_codes += rand
    image = image.filter(ImageFilter.BLUR)
    f = BytesIO()
    image.save(f, "png")
    data = f.getvalue()
    print("valid_codes:", keep_valid_codes)
    request.session["keep_valid_codes"] = keep_valid_codes
    return data


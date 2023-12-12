from PIL import Image, ImageDraw, ImageFont
import os
import random


class MemeGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path, text, author, width=500) -> str:
        try:
            with Image.open(img_path) as img:
                # Resize the image
                ratio = width / float(img.size[0])
                height = int(ratio * float(img.size[1]))
                img = img.resize((width, height), Image.NEAREST)

                # Add caption
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()

                caption = f'{text} - {author}'
                text_width, text_height = draw.textsize(caption, font=font)
                x = random.randint(0, width - text_width)
                y = random.randint(0, height - text_height)
                draw.text((x, y), caption, font=font, fill='white')

                # Save the image
                out_path = os.path.join(self.output_dir, f'meme_{random.randint(0, 1000000)}.jpg')
                img.save(out_path)

            return out_path
        except Exception as e:
            print(f'Error in make_meme: {e}')
            return ''

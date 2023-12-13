from PIL import Image, ImageDraw, ImageFont
import os
import random
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)


class MemeGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path, text, author, width=500) -> str:
        try:
            # Load the image and resize
            with Image.open(img_path) as img:
                ratio = width / float(img.size[0])
                height = int(ratio * float(img.size[1]))
                img = img.resize((width, height), Image.NEAREST)

                # Add text to the image
                draw = ImageDraw.Draw(img)
                font_path = 'arial.ttf'  # Ensure this is a valid path
                font = ImageFont.truetype(font_path, size=20)
                # Combine text and author
                full_text = f'{text} - {author}'

                # Get text size
                text_width = draw.textlength(full_text)

                # Ensure the text fits within the image
                max_x = img.width - text_width

                # Randomly choose text position
                x = random.randint(0, max(int(max_x), 1))  # Ensure max is not less than 0
                y = random.randint(20, img.height - 20)
                draw.text((x, y), full_text, font=font, fill='white')

                # Save the meme image
                out_path = os.path.join(self.output_dir, f'meme_{random.randint(0, 1000000)}.jpg')
                img.save(out_path)

            return out_path

        except Exception as e:
            logging.error(f'Error in make_meme: {e}')
            return ''

    from PIL import ImageFont

    def draw_text(self, draw, text, font_path, img_size):
        """
        Draws the text on the image with wrapping and random placement.
        """
        margin = 10
        width, height = img_size

        try:
            # Load font
            font = ImageFont.truetype(font_path, 20)
        except IOError:
            font = ImageFont.load_default()

        # Split text into words for wrapping
        words = text.split()
        lines = []
        line = ''
        while words:
            while words:
                test_line = line + words[0] + ' '
                # Measure text size
                text_width, text_height = draw.textsize(test_line, font=font)
                if text_width > width - 2 * margin:
                    break
                line = test_line
                words.pop(0)
            lines.append(line.strip())
            line = ''

        total_text_height = len(lines) * text_height
        y = random.randint(margin, height - total_text_height - margin)

        for line in lines:
            text_width, _ = draw.textsize(line, font=font)
            x = random.randint(margin, width - text_width - margin)
            draw.text((x, y), line, font=font, fill='white')
            y += text_height

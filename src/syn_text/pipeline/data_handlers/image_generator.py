import os
import random
from PIL import Image, ImageDraw, ImageFont

from syn_text.image_augmentations.beta_affine import RandomBetaAffine
from syn_text.image_augmentations.beta_perspective import RandomBetaPerspective
from syn_text.image_augmentations.erode import Erode


class ImageGenerator:
    def __init__(self, fonts, output_folder, apply_augmentation=False, apply_rotation=True):
        self.fonts = fonts
        self.output_folder = output_folder
        self.apply_augmentation = apply_augmentation
        self.apply_rotation = apply_rotation

        # Ensure the output folder exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def apply_random_augmentation(self, img: Image.Image) -> Image.Image:
        augmentations = [
            RandomBetaAffine(max_offset_ratio=0.2, alpha=2, beta=2),
            RandomBetaPerspective(max_offset_ratio=0.2, alpha=2, beta=2),
            Erode(filter_size_min=3, filter_size_max=5, alpha=1, beta=3)
        ]
        augmentation = random.choice(augmentations)
        return augmentation(img)

    def create_image_with_text(self, sentence, index):
        """Creates an image with the given sentence in a single line and auto-adjusted margins."""
        background_color = (255, 255, 255)  # White background
        text_color = (0, 0, 0)  # Black text

        # Randomly select a font from the list
        font_path = random.choice(self.fonts)
        try:
            font = ImageFont.truetype(font_path, 40)
        except:
            print(f"Could not load font {font_path}, using default font.")
            font = ImageFont.load_default()

        # Get text size
        text_size = font.getbbox(sentence)  # Get text bounding box
        text_width = text_size[2] - text_size[0]  # Width of text
        text_height = text_size[3] - text_size[1]  # Height of text

        # Apply random horizontal scaling (width adjustment)
        scale_factor = random.uniform(0.8, 1.2)  # Randomly scale text width between 80% and 120%
        text_width *= scale_factor  # Adjust the width
        text_height *= scale_factor  # Adjust the height proportionally

        # Add a small margin around the text
        margin_x = 20
        margin_y = 10
        img_width = int(text_width + (2 * margin_x))
        img_height = int(text_height + (2 * margin_y))

        # Create an image with dynamic size
        img = Image.new("RGB", (img_width, img_height), background_color)
        draw = ImageDraw.Draw(img)

        # Center text in the image
        text_x = margin_x
        text_y = margin_y
        draw.text((text_x, text_y), sentence, font=font, fill=text_color)

        # Optionally apply a random augmentation
        if self.apply_augmentation:
            img = self.apply_random_augmentation(img)

        # Optionally apply random rotation between 0 and 5 degrees
        if self.apply_rotation:
            rotation_angle = random.uniform(-5, 5)  # Random angle between 0 and 5 degrees
            img = img.rotate(rotation_angle, resample=Image.BICUBIC, expand=True)

        # Save image to the output folder
        filename = os.path.join(self.output_folder, f"sentence_{index}.png")
        img.save(filename)
        print(f"Image saved: {filename}")

from .beta_morphology import RandomBetaMorphology

from PIL import Image, ImageFilter


class Erode(RandomBetaMorphology):
    def __init__(self, filter_size_min: int = 3, filter_size_max: int = 5, alpha: float = 1, beta: float = 3):
        super().__init__(filter_size_min, filter_size_max, alpha, beta)

    def __call__(self, img: Image) -> Image:
        filter_size = self.sample_filter_size()
        return img.filter(ImageFilter.MinFilter(filter_size))
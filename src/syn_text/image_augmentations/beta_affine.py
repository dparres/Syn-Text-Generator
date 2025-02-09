from typing import Tuple, Union

from PIL import Image
from scipy.linalg import solve
import numpy as np


class RandomBetaAffine:
    """Apply a random affine transform on a PIL image using a Beta distribution."""

    def __init__(self, max_offset_ratio: float = 0.2, alpha: float = 2, beta: float = 2, fillcolor: Union[None, int, Tuple[int, int, int]] = None) -> None:
        assert max_offset_ratio > 0
        assert alpha > 0
        assert beta > 0
        self.max_offset_ratio = max_offset_ratio
        self.alpha = alpha
        self.beta = beta
        self.fillcolor = fillcolor

    def __call__(self, img: Image.Image) -> Image.Image:
        max_offset = min(img.size) * self.max_offset_ratio
        z = np.random.beta(self.alpha, self.beta, size=(3, 2))
        offset = ((2.0 * z - 1.0) * max_offset).astype(np.float32)
        w, h = img.size
        src = np.asarray([(0, 0), (0, h), (w, 0)], dtype=np.float32)
        dst = src + offset
        affine_mat = self.get_affine_transform(src, dst)
        return img.transform(
            img.size,
            method=Image.AFFINE,
            data=affine_mat,
            resample=Image.BILINEAR,
            fillcolor=self.fillcolor,
        )

    @staticmethod
    def get_affine_transform(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
        assert src.shape == (3, 2)
        assert dst.shape == (3, 2)
        coeffs = np.zeros((6, 6), dtype=np.float32)
        for i in [0, 1, 2]:
            coeffs[i, 0:2] = coeffs[i + 3, 3:5] = src[i]
            coeffs[i, 2] = coeffs[i + 3, 5] = 1
        return solve(coeffs, dst.transpose().flatten())

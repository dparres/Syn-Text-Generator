from PIL import Image
import numpy as np
from typing import Tuple, Union

class RandomBetaPerspective:
    def __init__(
        self,
        max_offset_ratio: float = 0.2,
        alpha: float = 2,
        beta: float = 2,
        fillcolor: Union[None, int, Tuple[int, int, int]] = None,
    ) -> None:
        assert max_offset_ratio > 0
        assert alpha > 0
        assert beta > 0
        self.max_offset_ratio = max_offset_ratio
        self.alpha = alpha
        self.beta = beta
        self.fillcolor = fillcolor

    def __call__(self, img: Image) -> Image:
        max_offset = min(img.size) * self.max_offset_ratio
        z = np.random.beta(self.alpha, self.beta, size=(4, 2))
        offset = ((2.0 * z - 1.0) * max_offset).astype(np.float32)
        w, h = img.size
        src = np.asarray([(0, 0), (0, h), (w, 0), (w, h)], dtype=np.float32)
        dst = src + offset
        perspective_transform = self.warp_perspective(src, dst)
        return img.transform(
            img.size,
            method=Image.PERSPECTIVE,
            data=perspective_transform,
            resample=Image.BILINEAR,
            fillcolor=self.fillcolor,
        )

    @repr
    def __repr__(self) -> str:
        return (
            f"vision.{self.__class__.__name__}("
            f"max_offset_ratio={self.max_offset_ratio}, "
            f"alpha={self.alpha}, beta={self.beta}"
            f"{f', fillcolor={self.fillcolor}' if self.fillcolor else ''})"
        )

    @staticmethod
    def warp_perspective(pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

        A = np.matrix(matrix, dtype=np.float32)
        B = np.array(pb).reshape(8)

        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)

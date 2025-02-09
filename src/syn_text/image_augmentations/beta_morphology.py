import scipy.special
import numpy as np

class RandomBetaMorphology:
    def __init__(self, filter_size_min: int, filter_size_max: int, alpha: float, beta: float):
        assert filter_size_min % 2 != 0, "Filter size must be odd"
        assert filter_size_max % 2 != 0, "Filter size must be odd"
        self.filter_size_min = filter_size_min
        self.filter_size_max = filter_size_max
        self.alpha = alpha
        self.beta = beta
        self.filter_sizes, self.filter_probs = self._create_filter_distribution(
            filter_size_min, filter_size_max, alpha, beta
        )

    @staticmethod
    def _create_filter_distribution(filter_size_min, filter_size_max, alpha, beta):
        n = (filter_size_max - filter_size_min) // 2 + 1
        if n < 2:
            return [filter_size_min], np.asarray([1.0], dtype=np.float32)
        filter_sizes = []
        filter_probs = []
        for k in range(n):
            filter_sizes.append(filter_size_min + 2 * k)
            filter_probs.append(
                scipy.special.comb(n, k) * scipy.special.beta(alpha + k, n - k + beta)
            )
        np_filter_probs = np.asarray(filter_probs, dtype=np.float32)

        # Normalize probabilities to sum to 1
        np_filter_probs /= np_filter_probs.sum()

        return filter_sizes, np_filter_probs

    def sample_filter_size(self):
        filter_size = np.random.choice(self.filter_sizes, p=self.filter_probs)
        return filter_size

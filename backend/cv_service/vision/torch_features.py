import numpy as np
import torch


class TorchTextureExtractor:
    """Deterministic torch feature extractor for skin texture signals.

    This avoids runtime model downloads while keeping the pipeline structured
    around tensors. A trained checkpoint can later replace this class without
    changing the REST contract.
    """

    def __init__(self) -> None:
        sobel_x = torch.tensor(
            [[[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]]],
            dtype=torch.float32,
        )
        sobel_y = torch.tensor(
            [[[-1.0, -2.0, -1.0], [0.0, 0.0, 0.0], [1.0, 2.0, 1.0]]],
            dtype=torch.float32,
        )
        self.sobel_x = sobel_x.unsqueeze(0)
        self.sobel_y = sobel_y.unsqueeze(0)

    @torch.inference_mode()
    def extract(self, gray_image: np.ndarray) -> dict[str, float]:
        tensor = torch.from_numpy(gray_image.astype("float32") / 255.0).unsqueeze(0).unsqueeze(0)
        grad_x = torch.nn.functional.conv2d(tensor, self.sobel_x, padding=1)
        grad_y = torch.nn.functional.conv2d(tensor, self.sobel_y, padding=1)
        magnitude = torch.sqrt(torch.square(grad_x) + torch.square(grad_y))
        return {
            "edge_mean": float(magnitude.mean().item()),
            "edge_p95": float(torch.quantile(magnitude.flatten(), 0.95).item()),
            "texture_std": float(tensor.std().item()),
        }

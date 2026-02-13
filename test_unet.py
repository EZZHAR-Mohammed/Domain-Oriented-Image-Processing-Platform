# test_unet.py
import cv2
import torch
import numpy as np
from filters.base_filter import BaseFilter  # Si tu as une classe BaseFilter

class UNet(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "U-Net Test"
        print("Chargement U-Net...")
        self.model = torch.hub.load('mateuszbuda/brain-segmentation-pytorch', 'unet', in_channels=3, out_channels=1, pretrained=True)
        self.model.eval()
        print("U-Net chargé OK")

    def apply(self, image, params):
        resized = cv2.resize(image, (256, 256))
        input_tensor = torch.from_numpy(resized.transpose((2, 0, 1))).float() / 255.0
        input_tensor = input_tensor.unsqueeze(0)

        with torch.no_grad():
            output = self.model(input_tensor)
            mask = (output > 0.5).float().squeeze().numpy() * 255
            mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
            mask = cv2.cvtColor(mask.astype(np.uint8), cv2.COLOR_GRAY2BGR)

        result = image.copy()
        result[mask == 255] = [0, 0, 255]
        return result

if __name__ == "__main__":
    print("Torch version:", torch.__version__)
    model = UNet()
    print("U-Net instancié OK")

    # Test sur une image (remplace par un chemin réel)
    img = cv2.imread("test_image.jpg")  # Mets une image de cellules ici
    if img is not None:
        result = model.apply(img, {})
        cv2.imwrite("unet_result.jpg", result)
        print("Test U-Net terminé → résultat sauvegardé : unet_result.jpg")
    else:
        print("Pas d'image test")
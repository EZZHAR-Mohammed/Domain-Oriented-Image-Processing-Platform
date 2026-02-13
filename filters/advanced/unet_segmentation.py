# filters/advanced/unet_segmentation.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter


class UNet(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "U-Net Segmentation (IA)"
        self.category = "Avancé / IA"
        self.description = "Segmentation sémantique avec modèle U-Net pré-entraîné (idéal pour cellules, tissus, anomalies)"
        self.model = None  # Chargement paresseux pour éviter crash au démarrage

    def load_model(self):
        if self.model is not None:
            return
        try:
            import torch
            print("Chargement U-Net (torch)...")
            self.model = torch.hub.load('mateuszbuda/brain-segmentation-pytorch', 'unet', in_channels=3, out_channels=1, pretrained=True)
            self.model.eval()
            print("U-Net chargé avec succès")
        except Exception as e:
            print(f"Erreur chargement U-Net : {e}")
            self.model = None

    def apply(self, image, params):
        self.load_model()  # Charge seulement quand on applique
        if self.model is None:
            print("U-Net non chargé → retour image originale")
            return image

        try:
            resized = cv2.resize(image, (256, 256))
            input_tensor = torch.from_numpy(resized.transpose((2, 0, 1))).float() / 255.0
            input_tensor = input_tensor.unsqueeze(0)

            with torch.no_grad():
                output = self.model(input_tensor)
                mask = (output > 0.5).float().squeeze().numpy() * 255
                mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
                mask = cv2.cvtColor(mask.astype(np.uint8), cv2.COLOR_GRAY2BGR)

            result = image.copy()
            result[mask == 255] = [0, 0, 255]  # Rouge sur zones segmentées
            return result
        except Exception as e:
            print(f"Erreur application U-Net : {e}")
            return image
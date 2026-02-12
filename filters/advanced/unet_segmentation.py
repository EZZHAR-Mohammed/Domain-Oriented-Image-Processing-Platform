# filters/advanced/unet_segmentation.py
import cv2
import torch
from filters.base_filter import BaseFilter


class UNet(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "U-Net Segmentation (IA)"
        self.category = "Avancé / IA"
        self.description = "Segmentation sémantique avec modèle U-Net pré-entraîné (pour cellules, tissus, etc.)"

        # Charge un modèle pré-entraîné (ex: pour segmentation cerveau – adapte pour biologie si besoin)
        self.model = torch.hub.load('mateuszbuda/brain-segmentation-pytorch', 'unet', in_channels=3, out_channels=1, pretrained=True)
        self.model.eval()  # Mode inférence

    def apply(self, image, params):
        # Préparation : resize à 256x256 (taille d'input U-Net)
        resized = cv2.resize(image, (256, 256))

        # Conversion en tensor
        input_tensor = torch.from_numpy(resized.transpose((2, 0, 1))).float() / 255.0
        input_tensor = input_tensor.unsqueeze(0)  # Ajout batch dimension

        with torch.no_grad():
            output = self.model(input_tensor)
            mask = (output > 0.5).float().squeeze().numpy() * 255  # Seuil à 0.5 pour binaire

        # Resize mask à taille originale
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
        mask = cv2.cvtColor(mask.astype(np.uint8), cv2.COLOR_GRAY2BGR)

        # Superposition : rouge pour les zones segmentées
        result = image.copy()
        result[mask == 255] = [0, 0, 255]
        return result

    def get_default_params(self):
        return {}
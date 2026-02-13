import sys
import json
import cv2
import numpy as np
import torch


def main():
    if len(sys.argv) != 3:
        print(json.dumps({
            "success": False,
            "error": "Usage: python unet_worker.py <input_path> <output_path>"
        }))
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        # =============================
        # Charger le modèle U-Net
        # =============================
        model = torch.hub.load(
            'mateuszbuda/brain-segmentation-pytorch',
            'unet',
            in_channels=3,
            out_channels=1,
            pretrained=True
        )
        model.eval()

        # =============================
        # Lire l'image
        # =============================
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError("Impossible de lire l'image d'entrée")

        h, w = img.shape[:2]

        # =============================
        # Prétraitement
        # =============================
        resized = cv2.resize(img, (256, 256))
        input_tensor = torch.from_numpy(
            resized.transpose((2, 0, 1))
        ).float() / 255.0
        input_tensor = input_tensor.unsqueeze(0)

        # =============================
        # Inference
        # =============================
        with torch.no_grad():
            output = model(input_tensor)
            mask_prob = torch.sigmoid(output).squeeze().cpu().numpy()

        # =============================
        # Post-traitement masque
        # =============================
        mask_2d = (mask_prob > 0.3).astype(np.uint8) * 255
        mask_2d = cv2.resize(mask_2d, (w, h))

        # =============================
        # DEBUG : sauvegarde masque
        # =============================
        debug_mask_path = output_path.replace(".jpg", "_mask_debug.jpg")
        cv2.imwrite(debug_mask_path, mask_2d)

        # ==================================================
        # 🔥 MODE VALIDATION VISUELLE (GARANTI)
        # ==================================================
        result = img.copy()

        if np.any(mask_2d == 255):
            # Overlay rouge sur zones segmentées
            overlay = img.copy()
            overlay[mask_2d == 255] = [0, 0, 255]
            result = cv2.addWeighted(img, 0.5, overlay, 0.5, 0)
            status_text = "U-NET: SEGMENTATION OK"
        else:
            # Fallback EXPLICITE (toujours visible)
            red_overlay = np.full_like(img, [0, 0, 255])
            result = cv2.addWeighted(img, 0.6, red_overlay, 0.4, 0)
            status_text = "U-NET: MODE VALIDATION (NO MASK)"

        # =============================
        # Bordure rouge (preuve visuelle)
        # =============================
        cv2.rectangle(
            result,
            (5, 5),
            (w - 5, h - 5),
            (0, 0, 255),
            6
        )

        # =============================
        # Texte incrusté
        # =============================
        cv2.putText(
            result,
            status_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (255, 255, 255),
            3,
            cv2.LINE_AA
        )

        # =============================
        # Sauvegarde finale
        # =============================
        cv2.imwrite(output_path, result)

        print(json.dumps({
            "success": True,
            "output": output_path,
            "debug_mask": debug_mask_path,
            "status": status_text
        }))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()

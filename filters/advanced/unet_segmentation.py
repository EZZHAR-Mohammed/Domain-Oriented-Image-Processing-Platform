import cv2
import subprocess
import json
import os
import sys
import tempfile
from filters.base_filter import BaseFilter


class UNet(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "U-Net Segmentation (IA)"
        self.category = "Avancé / IA"
        self.description = (
            "Segmentation sémantique avec modèle U-Net "
            "(overlay rouge + debug masque)"
        )

    def apply(self, image, params):
        # =============================
        # Fichiers temporaires
        # =============================
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_in:
            input_path = tmp_in.name
            cv2.imwrite(input_path, image)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_out:
            output_path = tmp_out.name

        try:
            # =============================
            # Lancement du worker
            # =============================
            proc = subprocess.run(
                [sys.executable, "unet_worker.py", input_path, output_path],
                capture_output=True,
                text=True,
                timeout=180,
                check=False
            )

            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()

            if stderr:
                print("Worker stderr:\n", stderr)

            # =============================
            # Lecture JSON
            # =============================
            json_line = ""
            for line in stdout.splitlines():
                if line.strip().startswith("{"):
                    json_line = line.strip()
                    break

            if not json_line:
                print("Aucun JSON valide trouvé.\nstdout:\n", stdout)
                return image

            parsed = json.loads(json_line)

            if not parsed.get("success"):
                print("Erreur worker :", parsed.get("error"))
                return image

            # =============================
            # Lire image résultat
            # =============================
            result_img = cv2.imread(parsed["output"])
            if result_img is None:
                print("Image résultat illisible")
                return image

            print("U-Net appliqué avec succès → masque rouge généré")
            debug_mask_path = parsed.get("debug_mask")
            print("Masque debug :", debug_mask_path)

            # Si un masque debug est fourni, l'utiliser pour créer
            # une vraie sortie de segmentation : conserver les
            # couleurs originales dans les zones segmentées et
            # mettre le reste en niveaux de gris.
            try:
                if debug_mask_path and os.path.exists(debug_mask_path):
                    mask = cv2.imread(debug_mask_path, cv2.IMREAD_GRAYSCALE)
                    if mask is None:
                        return result_img

                    # Normaliser le masque (0 ou 255)
                    _, mask_bin = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

                    # Diagnostics : afficher statistiques du masque pour debug
                    try:
                        import numpy as _np
                        unique, counts = _np.unique(mask_bin, return_counts=True)
                        stats = dict(zip([int(u) for u in unique.tolist()], counts.tolist()))
                        print(f"DEBUG mask stats: shape={mask_bin.shape}, uniques={stats}")

                        # Si le masque est entièrement blanc (255), la composition
                        # précédente retournait l'image originale (aucun effet visible).
                        # Dans ce cas, retourner l'image produite par le worker
                        # (overlay rouge + bordure) pour assurer une indication visuelle.
                        unique_vals = [int(u) for u in unique.tolist()]
                        if set(unique_vals) == {255}:
                            print("DEBUG: mask fully 255 — using worker overlay result for visibility")
                            return result_img
                    except Exception:
                        pass

                    # Préparer images
                    orig = image.copy()
                    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
                    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

                    # Composer : zones segmentées gardent la couleur
                    mask_3c = mask_bin[:, :, None]
                    composed = (orig * (mask_3c // 255) + gray_bgr * (1 - (mask_3c // 255))).astype('uint8')

                    return composed
                else:
                    return result_img
            except Exception:
                return result_img

        except Exception as e:
            print("Erreur lancement worker U-Net :", e)
            return image

        finally:
            # Nettoyage
            for f in [input_path, output_path]:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except:
                        pass

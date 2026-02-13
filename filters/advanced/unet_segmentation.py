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
            print("Masque debug :", parsed.get("debug_mask"))

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

# utils/report_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import cv2
import os
import datetime


def generate_pdf_report(original_img, processed_img, output_path, domain="Général", applied_filters=None):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # En-tête
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1*inch, height - 1*inch, f"Rapport de traitement d'image – {domain}")

    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.5*inch, f"Date : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Images côte à côte
    temp_orig = "temp_original.jpg"
    temp_proc = "temp_processed.jpg"
    cv2.imwrite(temp_orig, original_img)
    cv2.imwrite(temp_proc, processed_img)

    c.drawImage(temp_orig, 1*inch, height - 5*inch, width=3*inch, height=3*inch, preserveAspectRatio=True)
    c.drawImage(temp_proc, width - 4*inch, height - 5*inch, width=3*inch, height=3*inch, preserveAspectRatio=True)

    c.drawString(1*inch, height - 5.5*inch, "Image originale")
    c.drawString(width - 4*inch, height - 5.5*inch, "Image traitée")

    # ───────────────────────────────────────────────
    # Section Filtres appliqués + paramètres
    # ───────────────────────────────────────────────
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 6*inch, "Filtres appliqués :")

    c.setFont("Helvetica", 11)
    y = height - 6.5*inch
    if applied_filters and len(applied_filters) > 0:
        for idx, (filter_name, params) in enumerate(applied_filters, 1):
            c.drawString(1.2*inch, y, f"{idx}. {filter_name}")
            y -= 0.3*inch
            if params:
                param_str = ", ".join([f"{k}: {v}" for k, v in params.items()])
                c.drawString(1.4*inch, y, f"   Paramètres : {param_str}")
                y -= 0.3*inch
            y -= 0.1*inch
    else:
        c.drawString(1.2*inch, y, "Aucun filtre appliqué (ou image originale uniquement)")

    # Nettoyage fichiers temporaires
    if os.path.exists(temp_orig):
        os.remove(temp_orig)
    if os.path.exists(temp_proc):
        os.remove(temp_proc)

    c.save()
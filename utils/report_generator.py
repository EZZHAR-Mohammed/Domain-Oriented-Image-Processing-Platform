# utils/report_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import cv2
import os
import datetime


def generate_pdf_report(original_img, processed_img, output_path, domain="Général", applied_filters=None):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Titre
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 70, f"Rapport de traitement d'image – {domain}")

    # Date
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Date : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Images
    temp_orig = "temp_original.jpg"
    temp_proc = "temp_processed.jpg"
    cv2.imwrite(temp_orig, original_img)
    cv2.imwrite(temp_proc, processed_img)

    c.drawImage(temp_orig, 50, height - 350, width=250, height=200, preserveAspectRatio=True)
    c.drawImage(temp_proc, 320, height - 350, width=250, height=200, preserveAspectRatio=True)

    c.drawString(50, height - 380, "Image originale")
    c.drawString(320, height - 380, "Image traitée")

    # ───────────────────────────────────────────────
    # Nouveau : liste des filtres appliqués + params
    # ───────────────────────────────────────────────
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 420, "Filtres appliqués :")

    c.setFont("Helvetica", 10)
    y = height - 440
    if applied_filters:
        for filter_name, params in applied_filters:
            c.drawString(50, y, f"- {filter_name} avec params : {params}")
            y -= 20
    else:
        c.drawString(50, y, "Aucun filtre spécifique enregistré")

    # Nettoyage temps files
    os.remove(temp_orig) if os.path.exists(temp_orig) else None
    os.remove(temp_proc) if os.path.exists(temp_proc) else None

    c.save()
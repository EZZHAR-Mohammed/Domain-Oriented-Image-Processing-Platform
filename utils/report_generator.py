# utils/report_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet
import cv2
import os
import datetime
import numpy as np


def calculate_psnr(img1, img2):
    """Calcule le PSNR entre deux images (plus élevé = meilleure qualité)"""
    if img1.shape != img2.shape:
        return "N/A (tailles différentes)"
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return round(psnr, 2)


def generate_pdf_report(original_img, processed_img, output_path, domain="Général", applied_filters=None):
    """
    Génère un PDF clair et professionnel :
    - Images originale et traitée visibles côte à côte
    - Infos générales (date, taille, PSNR)
    - Tableau stylé des filtres + paramètres
    - Tout bien espacé et lisible
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.8*inch,
        leftMargin=0.8*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )
    elements = []
    styles = getSampleStyleSheet()

    # Titre principal (centré, gros, gras)
    title_style = styles['Title']
    title_style.fontSize = 22
    title_style.alignment = 1  # centré
    elements.append(Paragraph(f"Rapport de Traitement d'Image - {domain}", title_style))
    elements.append(Spacer(1, 0.5*inch))

    # Infos générales (date, taille image, PSNR)
    info_style = styles['Normal']
    info_style.fontSize = 12
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Date du rapport : {now}", info_style))
    elements.append(Spacer(1, 0.15*inch))

    if original_img is not None:
        h, w = original_img.shape[:2]
        elements.append(Paragraph(f"Taille de l'image : {w} × {h} pixels", info_style))
        elements.append(Spacer(1, 0.15*inch))

        psnr_value = calculate_psnr(original_img, processed_img)
        elements.append(Paragraph(f"PSNR (qualité de la transformation) : {psnr_value} dB", info_style))
        elements.append(Spacer(1, 0.4*inch))

    # Section : Comparaison visuelle (images côte à côte)
    elements.append(Paragraph("Comparaison visuelle :", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))

    # Chemins temporaires absolus pour éviter les problèmes de dossier
    temp_dir = os.path.dirname(output_path) or os.getcwd()
    temp_orig = os.path.join(temp_dir, "temp_original_export.jpg")
    temp_proc = os.path.join(temp_dir, "temp_processed_export.jpg")

    # Sauvegarde images temporaires
    cv2.imwrite(temp_orig, original_img)
    cv2.imwrite(temp_proc, processed_img)

    # Tableau pour afficher les deux images côte à côte
    img_data = [
        [
            ReportLabImage(temp_orig, width=3.2*inch, height=3.2*inch),
            ReportLabImage(temp_proc, width=3.2*inch, height=3.2*inch)
        ],
        ["Image originale", "Image après application des filtres"]
    ]

    img_table = Table(img_data, colWidths=[3.5*inch, 3.5*inch])
    img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.8, colors.grey),
        ('BACKGROUND', (0,1), (0,1), colors.lightgrey),
        ('BACKGROUND', (1,1), (1,1), colors.lightgrey),
        ('TEXTCOLOR', (0,1), (-1,1), colors.black),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 11),
    ]))
    elements.append(img_table)
    elements.append(Spacer(1, 0.6*inch))

    # Section : Tableau des filtres appliqués
    elements.append(Paragraph("Historique des filtres appliqués :", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))

    if applied_filters and len(applied_filters) > 0:
        table_data = [
            ["#", "Filtre appliqué", "Paramètres utilisés"]
        ]

        for idx, (filter_name, params) in enumerate(applied_filters, 1):
            param_str = ", ".join([f"{k}: {v}" for k, v in params.items()]) if params else "Aucun paramètre modifié"
            table_data.append([str(idx), filter_name, param_str])

        filter_table = Table(table_data, colWidths=[0.6*inch, 3.2*inch, 3.8*inch])
        filter_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),        # En-tête bleu foncé
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 14),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),     # Fond clair pour lignes
            ('GRID', (0,0), (-1,-1), 0.8, colors.black),
            ('ALIGN', (0,1), (0,-1), 'CENTER'),                    # Numéro centré
            ('ALIGN', (1,1), (1,-1), 'LEFT'),                      # Nom filtre à gauche
            ('ALIGN', (2,1), (2,-1), 'LEFT'),                      # Params à gauche
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightcyan]),  # Alternance blanc/cyan clair
            ('BOX', (0,0), (-1,-1), 1.2, colors.darkgray),
        ]))
        elements.append(filter_table)
    else:
        elements.append(Paragraph("Aucun filtre appliqué → image originale inchangée", styles['Normal']))

    # Génération finale du PDF
    doc.build(elements)

    # Nettoyage des fichiers temporaires APRÈS la génération
    for temp_file in [temp_orig, temp_proc]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass

    print(f"PDF parfait généré : {output_path}")
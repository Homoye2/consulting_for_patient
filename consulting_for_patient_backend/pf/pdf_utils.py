"""
Utilitaires pour la génération de PDF des ordonnances - Design Moderne
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils import timezone
from datetime import datetime


class OrdonnanceCanvas(canvas.Canvas):
    """Canvas personnalisé avec en-tête et pied de page"""
    
    def __init__(self, *args, **kwargs):
        self.ordonnance = kwargs.pop('ordonnance', None)
        canvas.Canvas.__init__(self, *args, **kwargs)
        
    def draw_header(self):
        """Dessiner l'en-tête avec bande colorée"""
        # Bande supérieure bleue
        self.setFillColor(colors.HexColor('#1e40af'))
        self.rect(0, A4[1] - 1.5*cm, A4[0], 1.5*cm, fill=True, stroke=False)
        
        # Titre "ORDONNANCE MÉDICALE" en blanc
        self.setFillColor(colors.white)
        self.setFont("Helvetica-Bold", 16)
        self.drawCentredString(A4[0]/2, A4[1] - 1*cm, "ORDONNANCE MÉDICALE")
        
    def draw_footer(self):
        """Dessiner le pied de page"""
        # Ligne horizontale
        self.setStrokeColor(colors.HexColor('#1e40af'))
        self.setLineWidth(1)
        self.line(2*cm, 2*cm, A4[0] - 2*cm, 2*cm)
        
        # Texte du pied de page
        self.setFillColor(colors.HexColor('#6b7280'))
        self.setFont("Helvetica", 8)
        
        if self.ordonnance:
            footer_text = f"Ordonnance N° {self.ordonnance.numero_ordonnance} - Générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
            self.drawCentredString(A4[0]/2, 1.5*cm, footer_text)
            
            # Mention légale
            self.setFont("Helvetica-Oblique", 7)
            self.drawCentredString(A4[0]/2, 1*cm, "Document médical confidentiel - Ne pas jeter sur la voie publique")
    
    def showPage(self):
        self.draw_header()
        self.draw_footer()
        canvas.Canvas.showPage(self)


def generer_pdf_ordonnance(ordonnance):
    """
    Génère un PDF pour une ordonnance donnée avec un design moderne
    """
    buffer = BytesIO()
    
    # Configuration du document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=3*cm
    )
    
    # Styles personnalisés
    styles = getSampleStyleSheet()
    
    # Style pour les titres de section avec fond coloré
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=10,
        spaceBefore=15,
        alignment=TA_CENTER
    )
    
    # Style pour les sous-titres
    subsection_style = ParagraphStyle(
        'SubSection',
        parent=styles['Heading3'],
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=6,
        spaceBefore=8
    )
    
    # Style pour le texte normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        leading=12
    )
    
    # Style pour les labels en gras
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#374151'),
        spaceAfter=4
    )
    
    # Style pour les informations importantes
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#4b5563'),
        spaceAfter=3,
        leading=11
    )
    
    # Contenu du PDF
    story = []
    
    # SECTION 1: Informations Hôpital et Prescripteur (disposition moderne)
    hopital_data = [
        [Paragraph("<b>ÉTABLISSEMENT DE SANTÉ</b>", subsection_style), 
         Paragraph("<b>PRESCRIPTEUR</b>", subsection_style)]
    ]
    
    hopital_info = f"""
    <b>{ordonnance.hopital.nom}</b><br/>
    <font size=9>{ordonnance.hopital.adresse}<br/>
    {ordonnance.hopital.ville}, {ordonnance.hopital.pays}<br/>
    <b>Tél:</b> {ordonnance.hopital.telephone}<br/>
    <b>Email:</b> {ordonnance.hopital.email}</font>
    """
    
    prescripteur_info = f"""
    <b>Dr. {ordonnance.specialiste.user.nom}</b><br/>
    <font size=9>{ordonnance.specialiste.titre}<br/>
    <b>Spécialité:</b> {ordonnance.specialiste.specialite.nom}<br/>
    <b>N° Ordre:</b> {ordonnance.specialiste.numero_ordre}</font>
    """
    
    hopital_data.append([
        Paragraph(hopital_info, info_style),
        Paragraph(prescripteur_info, info_style)
    ])
    
    header_table = Table(hopital_data, colWidths=[8.75*cm, 8.75*cm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#d1d5db')),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 0.4*cm))
    
    # SECTION 2: Informations de l'ordonnance ET du patient sur la même ligne
    # Créer le tableau pour les infos de l'ordonnance (gauche)
    ordonnance_data = [
        ['N° Ordonnance', ordonnance.numero_ordonnance],
        ['Date de prescription', ordonnance.date_prescription.strftime('%d/%m/%Y à %H:%M')],
        ['Valide jusqu\'au', ordonnance.date_expiration.strftime('%d/%m/%Y') if ordonnance.date_expiration else 'Non définie']
    ]
    
    ordonnance_table = Table(ordonnance_data, colWidths=[4*cm, 4.5*cm])
    ordonnance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#eff6ff')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e40af')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3b82f6')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bfdbfe')),
    ]))
    
    # Créer le tableau pour les infos du patient (droite)
    patient_data = [
        ['Nom complet', f"{ordonnance.patient_nom} {ordonnance.patient_prenom}"],
        ['Âge', f"{ordonnance.patient_age} ans"],
        ['Sexe', 'Masculin' if ordonnance.patient_sexe == 'M' else 'Féminin']
    ]
    
    patient_table = Table(patient_data, colWidths=[3.5*cm, 5*cm])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef3c7')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#92400e')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#f59e0b')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fde68a')),
    ]))
    
    # Combiner les deux tableaux sur la même ligne
    combined_data = [[ordonnance_table, patient_table]]
    combined_table = Table(combined_data, colWidths=[8.75*cm, 8.75*cm])
    combined_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(combined_table)
    story.append(Spacer(1, 0.5*cm))
    
    # SECTION 3: Médicaments prescrits (tableau moderne)
    story.append(Paragraph("PRESCRIPTION MÉDICALE", section_style))
    
    if ordonnance.lignes.exists():
        # En-tête du tableau des médicaments avec style moderne
        medicaments_data = [
            ['Médicament', 'Dosage', 'Forme', 'Qté', 'Posologie', 'Durée']
        ]
        
        # Données des médicaments
        for ligne in ordonnance.lignes.all():
            medicaments_data.append([
                Paragraph(f"<b>{ligne.nom_complet}</b>", info_style),
                ligne.dosage,
                ligne.get_unite_display(),
                f"{ligne.quantite}",
                Paragraph(ligne.get_frequence_display(), info_style),
                f"{ligne.duree_traitement}j" if ligne.duree_traitement else '-'
            ])
        
        # Créer le tableau avec design moderne
        medicaments_table = Table(medicaments_data, colWidths=[4.5*cm, 2*cm, 2*cm, 1.5*cm, 5*cm, 2.5*cm])
        medicaments_table.setStyle(TableStyle([
            # En-tête avec gradient simulé
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Corps du tableau
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Bordures
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1e40af')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1e3a8a')),
            ('INNERGRID', (0, 1), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            
            # Alternance de couleurs avec nuances subtiles
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        story.append(medicaments_table)
        story.append(Spacer(1, 0.4*cm))
        
        # Instructions détaillées pour chaque médicament (encadrés)
        instructions_trouvees = False
        for i, ligne in enumerate(ordonnance.lignes.all(), 1):
            if ligne.instructions:
                if not instructions_trouvees:
                    story.append(Paragraph("INSTRUCTIONS SPÉCIFIQUES", subsection_style))
                    instructions_trouvees = True
                
                instruction_text = f"<b>{i}. {ligne.nom_complet}:</b><br/>{ligne.instructions}"
                instruction_para = Paragraph(instruction_text, info_style)
                
                # Encadré pour chaque instruction
                instruction_table = Table([[instruction_para]], colWidths=[17.5*cm])
                instruction_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef9c3')),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#eab308')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(instruction_table)
                story.append(Spacer(1, 0.2*cm))
        
        if instructions_trouvees:
            story.append(Spacer(1, 0.2*cm))
    
    # SECTION 4: Recommandations (encadré important)
    if ordonnance.recommandations:
        story.append(Paragraph("RECOMMANDATIONS GÉNÉRALES", section_style))
        
        recommandation_para = Paragraph(ordonnance.recommandations, normal_style)
        recommandation_table = Table([[recommandation_para]], colWidths=[17.5*cm])
        recommandation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dbeafe')),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#3b82f6')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(recommandation_table)
        story.append(Spacer(1, 0.5*cm))
    
    # SECTION 5: Signature avec encadré
    story.append(Spacer(1, 0.8*cm))
    
    signature_text = f"""
    <b>Date et lieu:</b> {ordonnance.date_prescription.strftime('%d/%m/%Y')} - {ordonnance.hopital.ville}<br/>
    <br/>
    <b>Le Prescripteur</b><br/>
    Dr. {ordonnance.specialiste.user.nom}<br/>
    {ordonnance.specialiste.titre}<br/>
    <i>Signature et cachet professionnel</i>
    """
    
    signature_para = Paragraph(signature_text, ParagraphStyle(
        'SignatureStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_RIGHT,
        spaceAfter=0
    ))
    
    signature_table = Table([[signature_para]], colWidths=[17.5*cm])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(signature_table)
    
    # Note de validité
    story.append(Spacer(1, 0.5*cm))
    validite_style = ParagraphStyle(
        'ValiditeStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#dc2626'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    if ordonnance.date_expiration:
        validite_text = f"⚠ Cette ordonnance est valide jusqu'au {ordonnance.date_expiration.strftime('%d/%m/%Y')} ⚠"
        story.append(Paragraph(validite_text, validite_style))
    
    # Construire le PDF avec canvas personnalisé
    doc.build(story, canvasmaker=lambda *args, **kwargs: OrdonnanceCanvas(
        *args, ordonnance=ordonnance, **kwargs
    ))
    
    # Retourner le buffer
    buffer.seek(0)
    return buffer


def generer_nom_fichier_pdf(ordonnance):
    """
    Génère un nom de fichier approprié pour le PDF de l'ordonnance
    """
    date_str = ordonnance.date_prescription.strftime('%Y%m%d')
    patient_nom = ordonnance.patient_nom.replace(' ', '_')
    return f"Ordonnance_{ordonnance.numero_ordonnance}_{patient_nom}_{date_str}.pdf"
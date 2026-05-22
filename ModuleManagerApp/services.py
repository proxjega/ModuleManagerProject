from .models import Module, CustomUser
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from io import BytesIO

class ModuleLimitExceeded(Exception):
    pass

def create_module(user, data):
    module_count = Module.objects.filter(user=user).count()
    if module_count >= 20:
        raise ModuleLimitExceeded("You have reached the maximum of 20 modules.")

    module = Module.objects.create(
        user=user,
        title=data["title"],
        teacher=data["teacher"],
        description=data.get("description", ""),
        faculty=data.get("faculty", ""),
        module_type=data.get("module_type", Module.TYPE_COMPULSORY),
        delivery_mode=data.get("delivery_mode", Module.DELIVERY_F2F),
        language=data.get("language", Module.LANGUAGE_LT),
        credits=data.get("credits", 1)
    )
    module.save()
    return module

def redact_module(id, data):
    module = Module.objects.get(pk=id)
    module.teacher = data.get("teacher", module.teacher)
    module.description = data.get("description", module.description)
    module.faculty = data.get("faculty", module.faculty)
    module.module_type = data.get("module_type", module.module_type)
    module.delivery_mode = data.get("delivery_mode", module.delivery_mode)
    module.language = data.get("language", module.language)
    module.credits = data.get("credits", module.credits)
    module.save()

def delete_module(id):
    module = Module.objects.get(pk=id)
    module.delete()

def register_user(data):
    user = CustomUser.objects.create_user(
        username=data["username"],
        password=data["password1"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        study_institution=data["study_institution"],
        degree=data.get("degree", CustomUser.DEGREE_BACHELOR),
        name_of_program=data["name_of_program"],
        start_year=data["start_year"],
    )
    user.save()
    return user

def redact_profile(user, data):
    current_user = CustomUser.objects.get(pk=user.id)
    current_user.first_name = data.get("first_name", current_user.first_name)
    current_user.last_name = data.get("last_name", current_user.last_name)
    current_user.email = data.get("email", current_user.email)
    current_user.study_institution = data.get("study_institution", current_user.study_institution)
    current_user.degree=data.get("degree", current_user.degree)
    current_user.name_of_program = data.get("name_of_program", current_user.name_of_program)
    current_user.start_year = data.get("start_year", current_user.start_year)
    current_user.save()

def generate_pdf(module_id, data):
    module = Module.objects.get(pk=module_id)

    filename = data.get("filename", module.title)

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    elements = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=12,
        leading=14,
        spaceAfter=12,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
    )

    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
    )

    # title

    elements.append(
        Paragraph(
            "<b>COURSE UNIT (MODULE) DESCRIPTION</b>",
            title_style
        )
    )

    elements.append(Spacer(1, 10))

    # data

    data = [
        [
            Paragraph("<b>Course unit (module) title</b>", header_style),
        ],
        [
            Paragraph(module.title, normal_style),
        ],

        [
            Paragraph("<b>Lecturer(s)</b>", header_style),
            Paragraph(
                "<b>Department(s) where the course unit (module) is delivered</b>",
                header_style,
            ),
        ],
        [
            Paragraph(module.teacher, normal_style),
            Paragraph(module.faculty or "-", normal_style),
        ],

        [
            Paragraph("<b>Type</b>", header_style),
            Paragraph("<b>Mode of delivery</b>", header_style),
            Paragraph("<b>Language(s) of instruction</b>", header_style),
        ],
        [
            Paragraph(module.get_module_type_display(), normal_style),
            Paragraph(module.get_delivery_mode_display(), normal_style),
            Paragraph(module.get_language_display(), normal_style),
        ],

        [
            Paragraph("<b>Course (module) volume in credits</b>", header_style),
        ],
        [
            Paragraph(str(module.credits), normal_style),
        ],

         [
            Paragraph("<b>Purpose of the course unit (module):</b>", header_style),
        ],
        [
            Paragraph(str(module.description), normal_style),
        ],
    ]

    # TABLES

    table1 = Table(
        data[0:2],
        colWidths=[520],
    )

    table1.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    )

    elements.append(table1)
    elements.append(Spacer(1, 10))

    table2 = Table(
        data[2:4],
        colWidths=[260, 260],
    )

    table2.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    )

    elements.append(table2)
    elements.append(Spacer(1, 10))

    # Table 3: Type & Mode of Delivery & Language (3 columns)
    table3 = Table(
        data[4:6],
        colWidths=[173, 173, 174],
    )

    table3.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    )

    elements.append(table3)
    elements.append(Spacer(1, 10))

    table4 = Table(
        data[6:8],
        colWidths=[520],
    )

    table4.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    )

    elements.append(table4)
    elements.append(Spacer(1, 10))

    table5 = Table(
        data[8:10],
        colWidths=[520],
    )

    table5.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    )

    elements.append(table5)

    # build pdf

    doc.build(elements)

    pdf_buffer.seek(0)

    response = HttpResponse(
        pdf_buffer.getvalue(),
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}.pdf"'
    )

    return response
    
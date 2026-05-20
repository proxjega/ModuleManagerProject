from .models import Module, CustomUser
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO

def create_module(user, data):
    module = Module.objects.create(
        user=user,
        title=data["title"],
        teacher=data["teacher"],
        description=data.get("description", "")
    )
    module.save()
    return module

def redact_module(id, data):
    module = Module.objects.get(pk=id)
    module.teacher = data.get("teacher", module.teacher)
    module.description = data.get("description", module.description)
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
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#0d6e5a',
        spaceAfter=12,
        alignment=1  
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#0d6e5a',
        spaceAfter=6,
        spaceBefore=12,
    )
    body_style = styles['BodyText']
    
    elements.append(Paragraph(module.title, title_style))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("Teacher:", heading_style))
    elements.append(Paragraph(module.teacher, body_style))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("Description:", heading_style))
    description = module.description if module.description else "No description added."
    elements.append(Paragraph(description, body_style))
    
    doc.build(elements)
    
    pdf_buffer.seek(0)
    pdf_bytes = pdf_buffer.getvalue()
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    
    return response

    
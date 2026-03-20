from .models import Module, CustomUser

def create_module(user, data):
    module = Module.objects.create(
        user=user,
        title=data["title"],
        teacher=data["teacher"],
        description=data.get("description", "")
    )
    module.save()
    return module

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
    
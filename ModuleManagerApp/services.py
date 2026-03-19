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
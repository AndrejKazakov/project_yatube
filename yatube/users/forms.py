from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
# from users.models import CustomUser


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email', 'groups')

# class CreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('username', 'fio', 'type', 'location', 'check')

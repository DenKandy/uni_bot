from django import forms
from .models import UserUniModel

class UserUniForm(forms.ModelForm):
    class Meta:
        model = UserUniModel
        fields = [
            'user_types',
            'position_manager',
            'curatorship',
            'chair',
            'course',
            'group',
            'full_name',
            'phone_number',
            'telegram_id',
            'is_active'
            ]
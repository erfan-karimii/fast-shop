from django import forms
from .models import Comment
from home.models import Brand

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title','text','score')


class ProductFilterForm(forms.MultiValueField):
    def __init__(self, **kwargs):
        # Define one message for all fields.
        error_messages = {
            "incomplete": "Enter a country calling code and a phone number.",
        }
        # Or define a different message for each field.
        fields = (
            forms.CharField(
                error_messages={"incomplete": "Enter a phone number."},
                # validators=[RegexValidator(r"^[0-9]+$", "Enter a valid phone number.")],
            ),
            forms.CharField(
                # validators=[RegexValidator(r"^[0-9]+$", "Enter a valid extension.")],
                required=False,
            ),
        )
        super().__init__(
            error_messages=error_messages,
            fields=fields,
            require_all_fields=False,
            **kwargs
        )


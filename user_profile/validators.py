from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _, ngettext


class ListIncludesValidator:
    """
    Validate whether the password is of a includes chars in list.
    """

    def __init__(self, char_list: list, validator_name: str):
        self.char_list = char_list
        self.validator_name = validator_name

    def validate(self, password, user=None):
        for p in password:
            if p in self.char_list:
                return

        if self.validator_name == 'CAPITAL':
            raise ValidationError(
                ngettext(
                    "Пароль не содержит заглавную букву",
                    "Пароль не содержит заглавнух букв",
                    1
                ),
                code='not capital letters',
            )
        if self.validator_name == 'NUMBER':
            raise ValidationError(
                ngettext(
                    "Пароль не содержит цифру",
                    "Пароль не содержит цифр",
                    2
                ),
                code='not numbers',
            )

        if self.validator_name == 'PUNCTUATION':
            raise ValidationError(
                ngettext(
                    "Пароль не содержит знака препинания",
                    "Пароль не содержит знаков препинания",
                    2
                ),
                code='not punctuation marks',
            )

    def get_help_text(self):
        text = ""
        if self.validator_name == 'CAPITAL':
            text = ngettext(
                "Пароль не содержит заглавную букву",
                "Пароль не содержит заглавнух букв",
                1
            )
        if self.validator_name == 'NUMBER':
            text = ngettext(
                "Пароль не содержит цифру",
                "Пароль не содержит цифр",
                2
            )
        if self.validator_name == 'PUNCTUATION':
            text = ngettext(
                "Пароль не содержит знака препинания",
                "Пароль не содержит знаков препинания",
                2
            )
        return text


class MaximumLengthValidator:
    """
    Validate whether the password is of a maximum length.
    """
    def __init__(self, max_length=20):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    "This password is too long. It must contain no more than %(min_length)d character.",
                    "This password is too long. It must contain no more than %(min_length)d characters.",
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            "This password is too long. It must contain no more than %(min_length)d character.",
            "This password is too long. It must contain no more than %(min_length)d characters.",
            self.max_length
        ) % {'max_length': self.max_length}

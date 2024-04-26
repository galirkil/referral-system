from django.core.validators import RegexValidator


class LettersDigitsValidator(RegexValidator):
    regex = r"[a-zA-Z0-9]+$"
    message = 'Допустимы только цифры и буквы ASCII'


class PhoneValidator(RegexValidator):
    regex = r"^\+\d+$"
    message = "Номер телефона должен быть передан в формате: '+1234567890'"


class OnlyDigitsValidator(RegexValidator):
    regex = r"^\d+$"
    message = "Допустимы только цифры"

from django.forms import ValidationError


def validate_file_size(file):
    """
    Validates that the uploaded file does not exceed the size limit.

    Args:
        file: The uploaded file to validate.
    """

    file_size = file.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f'Max file size is {limit_mb} MB')
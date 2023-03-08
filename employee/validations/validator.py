from rest_framework.exceptions import ValidationError

# Assumption made that below are the mandatory fields.
mandatory_field = ['name', 'salary', 'department']

class ValidationManager:

    # validate the request body for post request
    def validate_create_request(self, data):
        if data is None:
            raise ValidationError('Missing request body')

        for field in mandatory_field:
            if field not in data:
                raise ValidationError('Missing mandatory field ' + field)


import newrelic.agent
from voluptuous import Schema, Required, Url

from constants import ExtractRequestFields


@newrelic.agent.function_trace()
def validate_extract_create_user_visit_input(request):
    schema = Schema({
        Required(ExtractRequestFields.Input.MERCHANT): {
            str: {
                Required(ExtractRequestFields.Input.MERCHANT_ID),
                Required(ExtractRequestFields.Input.MERCHANT_NAME),
            }
        },
        Required(ExtractRequestFields.Input.USER): {
            str: {
                Required(ExtractRequestFields.Input.USER_ID) : str
            },
        }
    })
    return schema(request.json)

@newrelic.agent.function_trace()
def validate_extract_all_user_visit_input(request):
    schema = Schema({
        Required(ExtractRequestFields.Input.MERCHANT): {
            str: {
                Required(ExtractRequestFields.Input.MERCHANT_ID): str,
                Required(ExtractRequestFields.Input.MERCHANT_NAME): str,
            }
        },
        Required(ExtractRequestFields.Input.USER): {
            str: {
                Required(ExtractRequestFields.Input.USER_ID)
            },
        }
    })
    return schema(request.json)


@newrelic.agent.function_trace()
def validate_extract_get_visit_input(request):
    schema = Schema({
        Required(ExtractRequestFields.Input.VISIT_ID): str,
    })
    return schema(request.json)
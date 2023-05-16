"""All views will extend this BaseAPIView View."""
from rest_framework import status
from rest_framework.views import exception_handler
from djangokafka.settings import logger
from common.utils import create_response, create_message
from colorama import Back, Fore, Style


def custom_exception_handler(exc, context):
    """Call REST framework's default exception handler to set a standard error response on error."""
    logger.info("inside of custom exception handler.")

    response = exception_handler(exc, context)

    # logger.error(f"=>Exception Context:- {context}")
    # logger.error(f"=>Exception Response:- {response}")
    # logger.error(f"=>Exception:- {exc}")
    print(Back.RED, Fore.BLACK, "Exception", Style.RESET_ALL, str(exc))
    print(Back.WHITE, Fore.BLACK, "Exception Context", Style.RESET_ALL, str(context))
    print(Back.WHITE, Fore.BLACK, "Exception Response", Style.RESET_ALL, str(response))

    # The exception handler function should either return a Response object,or None
    # If the handler returns None then the exception will be re-raised and
    # Django will return a standard HTTP 500 'server error' response.
    # so override the response None and return standard response with HTTP_400_BAD_REQUEST

    if response is None:
        return create_response(
            create_message(status_code=1), status.HTTP_400_BAD_REQUEST
        )

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        return create_response(
            create_message(status_code=1), status.HTTP_400_BAD_REQUEST
        )

    return create_response(
        create_message(message=response.data.get("detail")), response.status_code
    )

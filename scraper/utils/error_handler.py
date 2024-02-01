from config.config_loader import is_production
from utils.email_notifier import EmailNotifier
from config.logger_config import logger

def handle_exception(e, context_info=''):
    """
    Handles exceptions by logging and optionally sending an email notification.

    Args:
    - e: The exception object.
    - context_info: Additional context about the exception as a string.
    """
    import traceback

    # Format the error message
    error_message = f"{context_info}\n\n{traceback.format_exc()}"

    # Log the error
    logger.error(error_message)

    # Send email notification if in production
    if is_production:
        # Assuming you have a class or function for sending emails
        email_notifier = EmailNotifier()
        email_notifier.send_error_notification(error_message)

from notifications.models import Notification


def store_notification(sender, recipient, message, notification_type='info', redirect_URL='/Notifications/'):
    """
    Function to create and store a notification.

    :param sender: EmployeePersonalInfo object of the notification sender
    :param recipient: EmployeePersonalInfo object of the notification recipient
    :param message: Message content of the notification
    :param notification_type: Type of the notification (e.g., 'info', 'warning', 'error')
    :return: Notification object if successfully created, None otherwise
    """
    try:
        # Create the notification
        notification = Notification.objects.create(
            sender=sender,
            recipient=recipient,
            message=message,
            notification_type=notification_type,
            redirect=redirect_URL
        )
        return notification
    except Exception as e:
        return None

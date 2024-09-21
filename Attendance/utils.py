from datetime import datetime, timedelta

def get_date_range():
    today = datetime.today().date()  # Get only the date part, without time
    # Case 1: If today's date is before the 15th
    if today.day <= 15:
        # Start date is the 15th of the previous month
        first_day_of_current_month = today.replace(day=1)
        previous_month_last_day = first_day_of_current_month - timedelta(days=1)
        start_date = previous_month_last_day.replace(day=15)

        # End date is the 15th of the current month
        end_date = today.replace(day=15)

    # Case 2: If today's date is on or after the 15th
    else:
        # Start date is the 15th of the current month
        start_date = today.replace(day=15)

        # Calculate the next month's 15th as the end date
        if today.month == 12:  # Special case for December
            end_date = today.replace(year=today.year + 1, month=1, day=15)
        else:
            end_date = today.replace(month=today.month + 1, day=15)
    print(start_date, end_date)
    return start_date, end_date

def get_date_range_old():
    today = datetime.today().date()  # Get only the date part, without time

    if today.day == 15:
        # If today is the 15th, the date range is from the 15th to the 15th
        start_date = today.replace(day=15)
        end_date = today.replace(day=15)
    else:
        # Otherwise, the range is from the 15th of the previous month to the current date
        if today.day < 15:
            # If today is before the 15th, adjust to the previous month
            first_day_of_current_month = today.replace(day=1)
            previous_month_last_day = first_day_of_current_month - timedelta(days=1)
            start_date = previous_month_last_day.replace(day=15)
        else:
            # For dates after the 15th of the current month
            start_date = today.replace(day=15)
        end_date = today

    return start_date, end_date
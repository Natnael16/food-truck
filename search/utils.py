def validate_location_params(latitude, longitude, radius):
    """
    Validate latitude, longitude, and radius parameters for location filtering.

    Parameters:
    - latitude: Latitude coordinate to be validated.
    - longitude: Longitude coordinate to be validated.
    - radius: Radius to be validated.

    Returns:
    - bool: True if all parameters are valid, False otherwise.
    """
    try:
        latitude, longitude, radius = float(latitude), float(longitude), float(radius)
    except:
        return False
    
    # Check if latitude and longitude are within valid ranges
    if not (-90 <= latitude <= 90):
        return False  # Latitude is out of range
    if not (-180 <= longitude <= 180):
        return False  # Longitude is out of range
    
    return True


def parse_open_hours(open_hours_str):
    """
    Parse the string representation of open hours into a dictionary.

    Args:
        open_hours_str (str): String containing the open hours data in the format:
            "Day1-Day5:Start_Time1-End_Time1/Start_Time2-End_Time2;Day2/Day3/Day4:Start_Time1-End_Time1/Start_Time2-End_Time2;..."

    Returns:
        dict: A dictionary representing the parsed open hours data.
            The keys are the days of the week, and the values are lists of time slots.
            Each time slot is represented by a dictionary with 'start_time' and 'end_time'.
    """
    # Mapping of abbreviated days to full day names
    day_mapping = {
        "Mo": "Monday", "Tu": "Tuesday", "We": "Wednesday", 
        "Th": "Thursday", "Fr": "Friday", "Sa": "Saturday", "Su": "Sunday"
    }
    open_hours = {}

    for schedule in open_hours_str.split(';'):
        parts = schedule.split(':')
        if len(parts) != 2:
            continue

        day_part, hour_part = parts[0].strip(), parts[1].strip()
        
        days = set()
        if '/' in day_part:
            for day in day_part.split('/'):
                days.add(day_mapping.get(day, day))
        elif '-' in day_part:
            start_day, end_day = day_part.split('-')
            start_index = list(day_mapping.keys()).index(start_day)
            end_index = list(day_mapping.keys()).index(end_day)
            for index in range(start_index, end_index + 1):
                days.add(list(day_mapping.values())[index])
        else:
            days.add(day_mapping.get(day_part, day_part))
        
        time_slots = []
        
        for time_slot in hour_part.split('/'):
            start_time, end_time = time_slot.split('-')
            time_slots.append({"start_time": start_time, "end_time": end_time})

        for day in days:
            open_hours[day] = time_slots

    return open_hours

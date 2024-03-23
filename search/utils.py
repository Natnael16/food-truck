def validate_location_params(latitude , longitude,radius):
        try:
            latitude,longitude,radius = float(latitude),float(longitude),float(radius)
        except:
            return False
        if not (-90 <= latitude <= 90):
            return False  # Latitude is out of range
        if not (-180 <= longitude <= 180): 
            return False  # Longitude is out of range
        return True

def parse_open_hours(open_hours_str):
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
            days.add(day_mapping.get(day_part,day_part))
        
            
        time_slots = []
        
        for time_slot in hour_part.split('/'):
            start_time, end_time = time_slot.split('-')
            time_slots.append({"start_time": start_time, "end_time": end_time})

        for day in days:
            open_hours[day] = time_slots

    return open_hours



def validate_location(latitude : float, longitude: float):
        """
            Validate latitude and longitude values.
            Args:
                latitude (float): Latitude value.
                longitude (float): Longitude value.
            Returns:
                bool: True if latitude and longitude are valid, False otherwise.
        """
        if not (-90 <= latitude <= 90):
            return False  # Latitude is out of range
        if not (-180 <= longitude <= 180):
            return False  # Longitude is out of range
        return True
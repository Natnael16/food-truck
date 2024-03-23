from mongoengine import Document, StringField, ListField, DictField, PointField, DateTimeField

class FoodTruck(Document):
    STATUS_CHOICES = (
        ('APPROVED', 'Approved'),
        ('SUSPENDED', 'Suspended'),
        ('REQUESTED', 'Requested'),
        ('EXPIRED', 'Expired'),
    )
    FACILITY_TYPE_CHOICES = (
        ('Truck', 'Truck'),
        ('Push Cart', 'Push Cart'),
        ('Unknown', 'Unknown'),
    )

    # Define fields for FoodTruck document
    applicant = StringField(required=True, max_length=255)
    facility_type = StringField(required=True, max_length=100, choices=FACILITY_TYPE_CHOICES)
    location_description = StringField(required=True, max_length=255)
    address = StringField(required=True, max_length=255)
    status = StringField(required=True, max_length=50, choices=STATUS_CHOICES)
    food_items = ListField(StringField(max_length=255))
    approved_at = DateTimeField()
    location = PointField(required=True)  # GeoJSON Point field for location
    open_hours = DictField()

    # Define indexes for efficient querying
    meta = {
        'indexes': [
            {'fields': ['applicant']},  # Index on the 'applicant' field
            {'fields': ['location'], 'type': '2dsphere'}  # 2dsphere index for geospatial queries on 'location'
        ]
    }

    def __str__(self):
        # String representation of FoodTruck instance
        return "{} at {}".format(self.applicant, self.location_description)

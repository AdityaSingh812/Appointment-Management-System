class Appointment:
    """
    Represents a single appointment in the salon.
    """

    # Class-level constants
    APPT_TYPE_DESCS = ["Available", "Mens Cut", "Ladies Cut", "Mens Colouring", "Ladies Colouring"]
    APPT_TYPE_PRICES = [0, 40, 60, 40, 80]

    def __init__(self, day_of_week, start_time_hour):
        """
        Initialize an Appointment object.
        
        :param day_of_week: The day of the week for the appointment.
        :param start_time_hour: The start time (24-hour clock).
        """
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0
        self.day_of_week = day_of_week
        self.start_time_hour = start_time_hour

    # Getters
    def get_client_name(self):
        return self.client_name

    def get_client_phone(self):
        return self.client_phone

    def get_appt_type(self):
        return self.appt_type

    def get_day_of_week(self):
        return self.day_of_week

    def get_start_time_hour(self):
        return self.start_time_hour

    def get_appt_type_desc(self):
        """Returns the text description of the appointment type."""
        return self.APPT_TYPE_DESCS[self.appt_type]

    def get_end_time_hour(self):
        """Returns the end time (start time + 1)."""
        return self.start_time_hour + 1

    # Setters
    def set_client_name(self, name):
        self.client_name = name

    def set_client_phone(self, phone):
        self.client_phone = phone

    def set_appt_type(self, appt_type):
        self.appt_type = appt_type

    # Methods
    def schedule(self, client_name, client_phone, appt_type):
        """Schedules an appointment with client details and type."""
        self.client_name = client_name
        self.client_phone = client_phone
        self.appt_type = appt_type

    def cancel(self):
        """Cancels the appointment and resets to available."""
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0

    def format_record(self):
        """Returns a CSV-style string representation of the appointment."""
        return f"{self.client_name},{self.client_phone},{self.appt_type},{self.day_of_week},{self.start_time_hour}"

    def __str__(self):
        """Returns a formatted string representation of the appointment."""
        appt_desc = self.get_appt_type_desc()
        start_time = f"{self.start_time_hour:02}:00"
        end_time = f"{self.get_end_time_hour():02}:00"
        return f"{self.client_name:<20} {self.client_phone:<15} {self.day_of_week:<10} {start_time} - {end_time} {appt_desc}"

    @classmethod
    def get_appt_type_desc_and_price(cls, appt_type):
        """Returns the description and price of an appointment type."""
        if 0 <= appt_type < len(cls.APPT_TYPE_DESCS):
            desc = cls.APPT_TYPE_DESCS[appt_type]
            price = cls.APPT_TYPE_PRICES[appt_type]
            return f"{appt_type}: {desc} ${price}"
        return "Invalid appointment type"

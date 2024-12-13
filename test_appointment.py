import os
from appointment import Appointment


def create_weekly_calendar():
    """Create a weekly calendar with available appointment slots."""
    calendar = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for day in days:
        for hour in range(9, 17):  # Appointments are from 9 AM to 4 PM
            calendar.append(Appointment(day, hour))
    return calendar

def load_scheduled_appointments(calendar):
    """Loads previously scheduled appointments from a file."""
    filename = "appointments1.csv"
    print(f"Loading appointments from {filename}...")

    if not os.path.exists(filename):
        print("File not found. Ensure the file exists in the same folder.")
        return

    with open(filename, 'r') as file:
        lines = file.readlines()

    count = 0
    for line in lines:
        data = line.strip().split(',')
        if len(data) != 5:
            print(f"Skipping invalid line: {line}")
            continue

        name, phone, appt_type, day, start_hour = data
        appt_type = int(appt_type)
        start_hour = int(start_hour)

        # Ensure this function is defined
        appointment = find_appointment_by_time(calendar, day, start_hour)
        if appointment:
            appointment.schedule(name, phone, appt_type)
            count += 1

    print(f"{count} previously scheduled appointments have been loaded.")


def save_scheduled_appointments(calendar):
    """Save scheduled appointments to a file."""
    filename = input("Enter appointment filename: ").strip()
    if os.path.exists(filename):
        overwrite = input("File already exists. Do you want to overwrite it (Y/N)? ").strip().lower()
        if overwrite != "y":
            filename = input("Enter a new appointment filename: ").strip()

    with open(filename, "w") as file:
        count = 0
        for appt in calendar:
            if appt.get_appt_type() != 0:  # Only save booked appointments
                file.write(appt.format_record() + "\n")
                count += 1
        print(f"{count} scheduled appointments have been successfully saved.")

def find_appointment_by_time(calendar, day, start_hour):
    """
    Finds an appointment in the calendar by day and start hour.
    :param calendar: List of Appointment objects.
    :param day: Day of the week to search.
    :param start_hour: Start time (hour in 24-hour clock).
    :return: Matching Appointment object or None.
    """
    for appointment in calendar:
        if appointment.day_of_week == day and appointment.start_time_hour == start_hour:
            return appointment
    return None



def find_appointment(calendar, day, hour):
    """Find an appointment by day and start hour."""
    for appt in calendar:
        if appt.get_day_of_week() == day and appt.get_start_time_hour() == hour:
            return appt
    return None


def input_day_of_week():
    """Get a valid day of the week from the user."""
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    while True:
        day = input("Enter day of week: ").capitalize()
        if day in valid_days:
            return day
        print(f"Day must be one of: {', '.join(valid_days)}")


def input_start_hour():
    """Get a valid start hour from the user."""
    while True:
        try:
            hour = int(input("Enter start hour (24-hour clock, e.g., 9 for 9 AM): "))
            if 9 <= hour <= 16:
                return hour
            print("Hour must be between 9 and 16.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def schedule_appointment(calendar):
    """Schedule an appointment."""
    day = input_day_of_week()
    hour = input_start_hour()
    appointment = find_appointment(calendar, day, hour)

    if appointment and appointment.get_appt_type() == 0:  # Slot is available
        name = input("Client Name: ").strip()
        phone = input("Client Phone: ").strip()
        print("Appointment types:")
        for i, desc in enumerate(Appointment.APPT_TYPE_DESCS):
            if i != 0:  # Skip "Available"
                print(f"  {i}: {desc} ${Appointment.APPT_TYPE_PRICES[i]}")
        while True:
            try:
                appt_type = int(input("Type of Appointment: "))
                if 1 <= appt_type <= 4:
                    break
                print("Invalid appointment type. Please choose a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        appointment.schedule(name, phone, appt_type)
        print(f"Appointment for {name} has been scheduled for {day} at {hour}:00.")
    else:
        print("Sorry, that time slot is not available!")

def cancel_appointment(calendar):
    """Cancel an appointment."""
    day = input_day_of_week()
    hour = input_start_hour()
    appointment = find_appointment(calendar, day, hour)

    if appointment and appointment.get_appt_type() != 0:  # Slot is booked
        print(f"Appointment: {day} {hour}:00 - {hour + 1}:00 for {appointment.get_client_name()} has been canceled!")
        appointment.cancel()
    else:
        print("That time slot isn't booked and doesn't need to be canceled.")


def print_calendar_for_day(calendar):
    """Print all appointments for a specific day."""
    day = input_day_of_week()
    print(f"\nAppointments for {day}\n")
    print(f"{'Client Name':<20}{'Phone':<15}{'Day':<10}{'Start':<7}{'End':<7}{'Type'}")
    print("-" * 80)
    for appt in calendar:
        if appt.get_day_of_week() == day:
            print(appt)
    print()


def calculate_total_fees_for_day(calendar):
    """Calculate total fees for a specific day."""
    day = input_day_of_week()
    total_fees = sum(
        Appointment.APPT_TYPE_PRICES[appt.get_appt_type()]
        for appt in calendar
        if appt.get_day_of_week() == day and appt.get_appt_type() != 0
    )
    print(f"Total fees for {day}: ${total_fees:.2f}")


def calculate_total_weekly_fees(calendar):
    """Calculate total fees for the week."""
    total_fees = sum(
        Appointment.APPT_TYPE_PRICES[appt.get_appt_type()]
        for appt in calendar
        if appt.get_appt_type() != 0
    )
    print(f"Total weekly fees: ${total_fees:.2f}")


def main():
    """Main function for the appointment management system."""
    calendar = create_weekly_calendar()
    print("Starting the Appointment Manager System")
    print("Weekly calendar created")

    if input("Would you like to load previously scheduled appointments from a file (Y/N)? ").strip().lower() == "y":
        load_scheduled_appointments(calendar)

    while True:
        print("\n======================================")
        print("   Hair So Long Appointment Manager   ")
        print("======================================")
        print(" 1) Schedule an appointment")
        print(" 2) Cancel an appointment")
        print(" 3) Print calendar for a specific day")
        print(" 4) Calculate total fees for a day")
        print(" 5) Calculate total weekly fees")
        print(" 6) Find appointment by name")
        print(" 0) Exit the system")
        try:
            choice = int(input("Enter your selection: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            schedule_appointment(calendar)
        elif choice == 2:
            cancel_appointment(calendar)
        elif choice == 3:
            print_calendar_for_day(calendar)
        elif choice == 4:
            calculate_total_fees_for_day(calendar)
        elif choice == 5:
            calculate_total_weekly_fees(calendar)
        elif choice == 0:
            if input("Would you like to save all scheduled appointments to a file (Y/N)? ").strip().lower() == "y":
                save_scheduled_appointments(calendar)
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

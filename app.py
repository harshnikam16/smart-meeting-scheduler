# Application
import datetime
import calendar

class MeetingScheduler:
    def __init__(self, working_hours=(9, 17), holidays=None):
        self.working_hours = working_hours  
        self.holidays = holidays if holidays else []  
        self.schedule = {}  
    
    def is_working_day(self, date):
        if date.weekday() >= 5 or date in self.holidays:  
            return False
        return True
    
    def schedule_meeting(self, user, date, start_time, end_time):
        if not self.is_working_day(date):
            return "Cannot schedule on weekends or holidays."
        
        if start_time < self.working_hours[0] or end_time > self.working_hours[1]:
            return "Meeting time must be within working hours."
        
        meeting_start = datetime.datetime.combine(date, datetime.time(start_time))
        meeting_end = datetime.datetime.combine(date, datetime.time(end_time))
        
        if user not in self.schedule:
            self.schedule[user] = {}
        if date not in self.schedule[user]:
            self.schedule[user][date] = []
        
        for existing_start, existing_end in self.schedule[user][date]:
            if not (meeting_end <= existing_start or meeting_start >= existing_end):
                return "Meeting time overlaps with another meeting."
        
        self.schedule[user][date].append((meeting_start, meeting_end))
        self.schedule[user][date].sort()
        return "Meeting scheduled successfully."
    
    def get_available_slots(self, user, date):
        if not self.is_working_day(date):
            return "No available slots on weekends or holidays."
        
        booked_slots = self.schedule.get(user, {}).get(date, [])
        available_slots = []
        start_hour = self.working_hours[0]
        
        for start, end in booked_slots:
            if start.hour > start_hour:
                available_slots.append(f"{start_hour}:00 - {start.hour}:00")
            start_hour = end.hour
        
        if start_hour < self.working_hours[1]:
            available_slots.append(f"{start_hour}:00 - {self.working_hours[1]}:00")
        
        return available_slots if available_slots else "No available slots."
    
    def view_meetings(self, user):
        if user not in self.schedule:
            return "No meetings scheduled."
        
        result = "Upcoming Meetings:\n"
        for date, meetings in sorted(self.schedule[user].items()):
            result += f"{date.strftime('%Y-%m-%d')}:\n"
            for start, end in meetings:
                result += f"  {start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}\n"
        return result

scheduler = MeetingScheduler(holidays=[datetime.date(2025, 3, 17)])
user = "Alice"
date = datetime.date(2025, 3, 18)

print(scheduler.schedule_meeting(user, date, 10, 11))  
print("Available slots:", scheduler.get_available_slots(user, date))
print(scheduler.view_meetings(user))

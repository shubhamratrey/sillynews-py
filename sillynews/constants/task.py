class TaskStatus(object):
    PENDING = 'pending'
    COMPLETED = 'completed'
    DELETED = 'deleted'

    VALID_STATUSES = ((PENDING, 'Pending'), (COMPLETED, 'Completed'), (DELETED, 'Deleted'))


class ScheduleStatus(object):
    ACTIVE = 'active'
    DELETED = 'deleted'

    VALID_STATUSES = ((ACTIVE, 'Active'), (DELETED, 'Deleted'))


class DayOfWeek(object):
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'

    VALID_DAYS = ((MONDAY, 'Monday'), (TUESDAY, 'Tuesday'), (WEDNESDAY, 'Wednesday'), (THURSDAY, 'Thursday'), (FRIDAY, 'Friday'),
                    (SATURDAY, 'Saturday'), (SUNDAY, 'Sunday'))

    ALL_DAY = (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)


DAYS_OF_WEEK = DayOfWeek()
TASK_STATUSES = TaskStatus()
SCHEDULE_STATUSES = ScheduleStatus()

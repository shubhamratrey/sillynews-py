class TaskStatus(object):
    PENDING = 'pending'
    COMPLETED = 'completed'
    DELETED = 'deleted'

    VALID_STATUSES = ((PENDING, 'Pending'), (COMPLETED, 'Completed'), (DELETED, 'Deleted'))


class ScheduleStatus(object):
    ACTIVE = 'active'
    DELETED = 'deleted'

    VALID_STATUSES = ((ACTIVE, 'Active'), (DELETED, 'Deleted'))


TASK_STATUSES = TaskStatus()
SCHEDULE_STATUSES = ScheduleStatus()

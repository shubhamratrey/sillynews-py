from django.core.paginator import Paginator, InvalidPage
from home.models import Schedule, Task
from constants import TASK_STATUSES


class TaskHelper(object):

    @staticmethod
    def get_schedules(profile_id, page_no=1, page_size=20, day=None):
        schedule_list = []
        schedules = Schedule.objects.filter(profile_id=profile_id)
        if day:
            schedules = schedules.filter(days=day)
        schedules = schedules.order_by('-start_time')
        paginator = Paginator(schedules, page_size)
        has_next = page_no < paginator.num_pages

        try:
            _schedules = paginator.page(page_no)
        except InvalidPage:
            return has_next, schedule_list
        for _schedule in _schedules:
            schedule = _schedule.to_json()
            schedule_list.append(schedule)
        return has_next, schedule_list

    @staticmethod
    def get_task(profile_id, page_no=1, page_size=20):
        task_list = []
        tasks = Task.objects.filter(profile_id=profile_id).order_by('-rank')
        paginator = Paginator(tasks, page_size)
        has_next = page_no < paginator.num_pages

        try:
            _tasks = paginator.page(page_no)
        except InvalidPage:
            return has_next, task_list
        for _task in _tasks:
            task = _task.to_json()
            if _task.schedule:
                task['schedule'] = _task.schedule.to_json()
            task_list.append(task)
        return has_next, task_list

    @staticmethod
    def get_schedules_comp_perc(schedules_ids):
        total_task = Task.objects.filter(schedule_id__in=schedules_ids).count()
        completed_task = Task.objects.filter(schedule_id__in=schedules_ids, status=TASK_STATUSES.COMPLETED).count()

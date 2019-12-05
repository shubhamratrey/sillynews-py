from django.core.paginator import Paginator, InvalidPage
from django.db.models import Count, Q

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
    def get_scheduled_task(schedule_id, page_no=1, page_size=1000):
        task_list = []
        tasks = Task.objects.filter(schedule_id=schedule_id).order_by('-rank')
        paginator = Paginator(tasks, page_size)
        has_next = page_no < paginator.num_pages

        try:
            _tasks = paginator.page(page_no)
        except InvalidPage:
            return has_next, task_list

        task_list = [_task.to_json() for _task in _tasks]
        return has_next, task_list

    @staticmethod
    def get_schedules_comp_perc(schedules_ids):
        status = Count('id', filter=Q(status=TASK_STATUSES.COMPLETED))
        tasks = list(Task.objects.filter(schedule_id__in=schedules_ids).values('schedule_id').annotate(total=Count('id'),
                                                                                             completed=status))
        percentage_count = dict()
        for task in tasks:
            percentage_count[task.get('schedule_id')] = int(round(task.get('completed') / task.get('total'), 2) * 100)
        return percentage_count

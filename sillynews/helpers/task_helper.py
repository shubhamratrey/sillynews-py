from django.core.paginator import Paginator, InvalidPage
from home.models import Schedule, Task


class TaskHelper(object):

    @staticmethod
    def get_schedules(profile_id, page_no=1, page_size=20):
        schedule_list = []
        schedules = Schedule.objects.filter(profile_id=profile_id).order_by('-time')
        paginator = Paginator(schedules, page_size)
        has_next = page_no < paginator.num_pages

        try:
            _schedules = paginator.page(page_no)
        except InvalidPage:
            return has_next, schedule_list
        for _schedule in _schedules:
            schedule = _schedule.to_json()
            schedule['comp_perc'] = 20
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
            task['schedule'] = _task.schedule.to_json()
            task_list.append(task)
        return has_next, task_list

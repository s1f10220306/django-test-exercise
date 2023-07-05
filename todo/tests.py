from django.test import TestCase,Client
from django.utils import timezone
from datetime import datetime
from todo.models import Task

# Create your tests here.
class SampleTestCase(TestCase):
    def test_sample(self):
        self.assertEqual(1 + 2, 3)

class TaskModelTestCase(TestCase):
    def test_index_get(self):
        client = Client()
        responese = client.get('/')

        self.assertEqual(responese.status_code, 200)
        self.assertEqual(responese.templates[0].name, 'todo/index.html' )
        self.assertEqual(len(responese.context['tasks']), 0)

    def test_create_task1(self):
        due = timezone.make_aware(datetime(2023, 6, 30, 23, 59, 59))
        task = Task(title='task1', due_at=due)
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task1')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, due)

    def test_create_task2(self):
        task = Task(title='task2')
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task2')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, None)

    def test_is_overdue_future(self):
        due = timezone.make_aware(datetime(2023, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2023, 6, 30, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertFalse(task.is_overdue(current))
        
    def test_is_overdue_past(self):
        due = timezone.make_aware(datetime(2023, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertTrue(task.is_overdue(current))

    def test_is_over_none(self):
        current = timezone.make_aware(datetime(2023, 7, 1, 0, 0, 0))
        task = Task(title='task1')
        task.save()

        self.assertFalse(task.is_overdue(current))

    def test_index_post(self):
        client = Client()
        data= {'title': 'Test Task', 'due_at' : '2023-06-30 23:59:59'}
        responese = client.post('/', data)

        self.assertEqual(responese.status_code,200)
        self.assertEqual(responese.templates[0].name, 'todo/index.html')
        self.assertEqual(len(responese.context['tasks']), 1)

    def test_index_get_order_post(self):
        task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2023, 7,1)))
        task1.save()
        task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2023, 8,1)))
        task2.save()
        client = Client()
        responese = client.get('/?order=post')

        self.assertEqual(responese.status_code, 200)
        self.assertEqual(responese.templates[0].name, 'todo/index.html')
        self.assertEqual(responese.context['tasks'][0], task2)
        self.assertEqual(responese.context['tasks'][1], task1)

    def test_index_get_order_due(self):
        task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2023, 7,1)))
        task1.save()
        task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2023, 8,1)))
        task2.save()
        client = Client()
        responese = client.get('/?order=post')

        self.assertEqual(responese.status_code, 200)
        self.assertEqual(responese.templates[0].name, 'todo/index.html')
        self.assertEqual(responese.context['tasks'][0], task1)
        self.assertEqual(responese.context['tasks'][1], task2)
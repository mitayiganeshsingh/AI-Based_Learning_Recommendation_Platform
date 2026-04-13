import csv
from django.core.management.base import BaseCommand
from core.models import Course, Skill
import os

class Command(BaseCommand):
    help = 'Seeds the database with initial course data'

    def handle(self, *args, **kwargs):
        csv_path = 'courses_dataset.csv'
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_path}'))
            return

        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                course, created = Course.objects.get_or_create(
                    title=row['title'],
                    defaults={
                        'description': row['description'],
                        'category': row['category'],
                        'popularity_score': float(row['popularity'])
                    }
                )
                
                # Handling skills
                skills = row['skills'].split(';')
                for skill_name in skills:
                    skill, _ = Skill.objects.get_or_create(name=skill_name.strip())
                    course.skills_taught.add(skill)
                
                course.save()
                
        self.stdout.write(self.style.SUCCESS('Successfully seeded course data'))

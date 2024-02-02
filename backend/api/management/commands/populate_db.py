# api/management/commands/populate_db.py
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import Department, Course, Section, SectionDetails, SectionDays, SectionChain, SectionChainDays

class Command(BaseCommand):
    help = 'Populate the database from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        self.populate_database(file_path)

    def populate_database(self, file_path):
        # Clear existing data from all relevant models
        Department.objects.all().delete()
        Course.objects.all().delete()
        Section.objects.all().delete()
        SectionDetails.objects.all().delete()
        SectionDays.objects.all().delete()
        SectionChain.objects.all().delete()
        SectionChainDays.objects.all().delete()

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                # Split each row using '!!' as the delimiter
                row = ''.join(row).split('!!')

                # Unpack row data
                dept_id, course_code, section_id, course_name, course_credits, course_days, start_time, end_time, instructor, location, alt_location, alt_days, alt_start, alt_end, total_seats, available_seats = row

                # Only add if int(course_code[:3]) < 500
                if int(course_code[:3]) < 500:
                    department, _ = Department.objects.get_or_create(dept_id=dept_id)

                    course, _ = Course.objects.get_or_create(
                        dept=department,
                        course_code=course_code,
                        defaults={
                            'course_name': course_name,
                            'course_credits': int(course_credits) if course_credits != 'None' else None,
                        }
                    )

                    section = Section.objects.create(
                        course=course,
                        section_id=section_id,
                        available_seats=int(available_seats) if available_seats != 'None' else None,
                        total_seats=int(total_seats) if total_seats != 'None' else None
                    )

                    # Check if location, start_time, and end_time are "None" strings
                    if location == 'None' or start_time == 'None' or end_time == 'None':
                        location = start_time = end_time = None

                    if location and start_time and end_time:
                        # Create SectionDetails instance
                        section_details = SectionDetails.objects.create(
                            section=section,
                            location=location,
                            instructor=instructor if instructor != 'None' else None,
                            start_time=datetime.strptime(start_time, '%H:%M').time() if start_time and start_time != 'None' else None,
                            end_time=datetime.strptime(end_time, '%H:%M').time() if end_time and end_time != 'None' else None
                        )

                        # Create SectionDays
                        for day in eval(course_days)[0]:
                            SectionDays.objects.create(
                                section=section,
                                day=day
                            )

                    # Check if alt_location, alt_start, and alt_end are "None" strings
                    if alt_location == 'None' or alt_start == 'None' or alt_end == 'None':
                        alt_location = alt_start = alt_end = None

                    if alt_location and alt_start and alt_end:
                        section_chain = SectionChain.objects.create(
                            section=section,
                            alt_location=alt_location,
                            alt_start_time=datetime.strptime(alt_start, '%H:%M').time(),
                            alt_end_time=datetime.strptime(alt_end, '%H:%M').time(),
                        )

                        # Create SectionChainDays
                        for alt_day in eval(alt_days)[0]:
                            SectionChainDays.objects.create(
                                section_chain=section_chain,
                                alt_day=alt_day
                            )

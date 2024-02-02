# api/management/commands/retrieve_sections.py

import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Department, Course, Section, SectionDetails, SectionDays, SectionChain, SectionChainDays

class Command(BaseCommand):
    help = 'Retrieve all sections from a department'

    def add_arguments(self, parser):
        parser.add_argument('dept_id', type=str, help='Department ID to retrieve sections from')
        parser.add_argument('output_file', type=str, help='Output file to write the section information')

    def handle(self, *args, **kwargs):
        dept_id = kwargs['dept_id']
        output_file = kwargs['output_file']
        sections_df = self.retrieve_sections(dept_id)
        sections_df.to_csv(output_file, index=False)
        self.stdout.write(f"Section information written to {output_file}")

    def retrieve_sections(self, dept_id):
        # Retrieve the department
        department = Department.objects.get(dept_id=dept_id)

        # Retrieve all courses belonging to the department
        courses = Course.objects.filter(dept=department)

        # Initialize lists to store section information
        data = {
            'Course Code': [],
            'Course Name': [],
            'Section ID': [],
            'Available Seats': [],
            'Total Seats': [],
            'Location': [],
            'Instructor': [],
            'Start Time': [],
            'End Time': [],
            'Days': [],
            'Alt Location': [],
            'Alt Start Time': [],
            'Alt End Time': [],
            'Alt Days': []
        }

        # Iterate over each course to retrieve its sections
        for course in courses:
            sections = Section.objects.filter(course=course)

            # Iterate over each section to retrieve its details
            for section in sections:
                try:
                    section_details = SectionDetails.objects.get(section=section)
                except SectionDetails.DoesNotExist:
                    section_details = None

                section_days = SectionDays.objects.filter(section=section)

                # Retrieve SectionChain if exists
                section_chain = SectionChain.objects.filter(section=section).first()
                if section_chain:
                    section_chain_days = SectionChainDays.objects.filter(section_chain=section_chain)
                else:
                    section_chain_days = None

                # Append section information to the data lists
                data['Course Code'].append(course.course_code)
                data['Course Name'].append(course.course_name)
                data['Section ID'].append(section.section_id)
                data['Available Seats'].append(section.available_seats)
                data['Total Seats'].append(section.total_seats)
                data['Location'].append(section_details.location if section_details else None)
                data['Instructor'].append(section_details.instructor if section_details else None)
                data['Start Time'].append(section_details.start_time.strftime('%H:%M') if section_details and section_details.start_time else None)
                data['End Time'].append(section_details.end_time.strftime('%H:%M') if section_details and section_details.end_time else None)
                data['Days'].append([day.day for day in section_days])
                data['Alt Location'].append(section_chain.alt_location if section_chain else None)
                data['Alt Start Time'].append(section_chain.alt_start_time.strftime('%H:%M') if section_chain and section_chain.alt_start_time else None)
                data['Alt End Time'].append(section_chain.alt_end_time.strftime('%H:%M') if section_chain and section_chain.alt_end_time else None)
                data['Alt Days'].append([day.alt_day for day in section_chain_days] if section_chain_days else None)

        # Create DataFrame from the data
        sections_df = pd.DataFrame(data)

        return sections_df

# api/management/commands/retrieve_data.py
from django.core.management.base import BaseCommand
import pandas as pd
from api.models import Department, Course, Section, SectionDetails, SectionDays, SectionChain, SectionChainDays

class Command(BaseCommand):
    help = 'Retrieve data from models and write it to a text file'

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str, help='Path to the output text file')

    def handle(self, *args, **kwargs):
        output_file = kwargs['output_file']
        with open(output_file, 'w') as f:
            f.write(self.get_departments())
            f.write(self.get_courses())
            f.write(self.get_sections())
            f.write(self.get_section_details())
            f.write(self.get_section_days())
            f.write(self.get_section_chains())
            f.write(self.get_section_chain_days())

    def get_dataframe(self, model):
        objects = model.objects.all()
        data = [obj.__dict__ for obj in objects]
        data = [{k: v for k, v in item.items() if not k.startswith('_')} for item in data]
        df = pd.DataFrame(data)
        return df

    def get_departments(self):
        return "Departments:\n" + self.get_dataframe(Department).to_string(index=False) + "\n\n"

    def get_courses(self):
        return "Courses:\n" + self.get_dataframe(Course).to_string(index=False) + "\n\n"

    def get_sections(self):
        return "Sections:\n" + self.get_dataframe(Section).to_string(index=False) + "\n\n"

    def get_section_details(self):
        return "Section Details:\n" + self.get_dataframe(SectionDetails).to_string(index=False) + "\n\n"

    def get_section_days(self):
        return "Section Days:\n" + self.get_dataframe(SectionDays).to_string(index=False) + "\n\n"

    def get_section_chains(self):
        return "Section Chains:\n" + self.get_dataframe(SectionChain).to_string(index=False) + "\n\n"

    def get_section_chain_days(self):
        return "Section Chain Days:\n" + self.get_dataframe(SectionChainDays).to_string(index=False) + "\n\n"

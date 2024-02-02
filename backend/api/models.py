from django.db import models

class Department(models.Model):
    dept_id = models.CharField(primary_key=True, max_length=10)

    def __str__(self):
        return str(self.dept_id)

class Course(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    course_credits = models.IntegerField()

    class Meta:
        unique_together = (('dept', 'course_code'),)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_id = models.CharField(max_length=10)
    available_seats = models.IntegerField()
    total_seats = models.IntegerField()

    class Meta:
        unique_together = (('course', 'section_id'),)

    def __str__(self):
        return f"{self.course.course_code} - {self.section_id}"

class SectionDetails(models.Model):
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    instructor = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.section.section_id}"

class SectionDays(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)

    class Meta:
        unique_together = (('section', 'day'),)

    def __str__(self):
        return f"{self.section} - {self.day}"

class SectionChain(models.Model):
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    alt_location = models.CharField(max_length=100)
    alt_start_time = models.TimeField()
    alt_end_time = models.TimeField()

    def __str__(self):
        return str(self.section)

class SectionChainDays(models.Model):
    section_chain = models.ForeignKey(SectionChain, on_delete=models.CASCADE)
    alt_day = models.CharField(max_length=10)

    class Meta:
        unique_together = (('section_chain', 'alt_day'),)

    def __str__(self):
        return f"{self.section_chain} - {self.alt_day}"

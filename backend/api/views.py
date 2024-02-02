# backend/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, SectionDays, SectionChainDays, Section, SectionChain, SectionDetails
from .serializers import CourseSerializer
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from itertools import combinations


@api_view(['GET'])  # Change POST to GET
def retrieve_courses(request):
    try:
        # Get the department ID and course code from the query parameters
        input_str = request.query_params.get('course', '').upper()
        
        # Extract department ID and course code
        dept_id = input_str[:4].strip()  # First 4 characters as department ID
        course_code = input_str[4:].strip()  # Remaining characters as course code
        
        if len(dept_id) == 4:
            # Query courses that match the provided department ID exactly
            courses = Course.objects.filter(dept_id=dept_id, course_code__startswith=course_code)
            
            # Serialize the courses
            serializer = CourseSerializer(courses, many=True)
            
            return JsonResponse({"courses": serializer.data})
        else:
            return JsonResponse({"error": "Department ID should be exactly 4 characters long."})
    
    except Exception as e:
        return JsonResponse({"error": str(e)})


@api_view(['GET'])
def add_course(request):
    try:
        course_id = request.query_params.get('id')
        course = Course.objects.prefetch_related('section_set__sectiondetails', 'section_set__sectionchain').get(id=course_id)

        # Serialize course data
        course_data = {
            "id": course.id,
            "course_code": course.course_code,
            "course_name": course.course_name,
            "course_credits": course.course_credits,
            "dept": course.dept.dept_id
        }

        sections_data = []
        for section in course.section_set.all():
            section_data = {
                "id": section.id,
                "section_id": section.section_id,
                "location": None,
                "instructor": None,
                "start_time": None,
                "end_time": None,
                "alt_location": None,
                "alt_start_time": None,
                "alt_end_time": None,
                "section_days": "",
                "alt_days": ""
            }

            try:
                # Check if sectiondetails exist and update attributes if they do
                sectiondetails = section.sectiondetails
                if sectiondetails:
                    section_data.update({
                        "location": sectiondetails.location[-4:],
                        "instructor": sectiondetails.instructor,
                        "start_time": sectiondetails.start_time.strftime('%I:%M %p') if sectiondetails.start_time else None,
                        "end_time": sectiondetails.end_time.strftime('%I:%M %p') if sectiondetails.end_time else None,
                    })

                # Fetch and serialize section days
                section_days = SectionDays.objects.filter(section=section)
                section_data["section_days"] = ''.join([day.day for day in section_days][::-1])

            except ObjectDoesNotExist:
                pass

            try:
                # Check if sectionchain exists and update attributes if they do
                sectionchain = section.sectionchain
                if sectionchain:
                    section_data.update({
                        "alt_location": sectionchain.alt_location[-4:],
                        "alt_start_time": sectionchain.alt_start_time.strftime('%I:%M %p') if sectionchain.alt_start_time else None,
                        "alt_end_time": sectionchain.alt_end_time.strftime('%I:%M %p') if sectionchain.alt_end_time else None,
                    })

                # Fetch and serialize alt days
                section_chain = section.sectionchain
                if section_chain:
                    alt_days = SectionChainDays.objects.filter(section_chain=section_chain)
                    section_data["alt_days"] = ''.join([day.alt_day for day in alt_days][::-1])
            except ObjectDoesNotExist:
                pass
    
            sections_data.append(section_data)

        return Response({"courseData": course_data, "sectionsData": sections_data})

    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)})

@api_view(['GET'])
def filter_sections(request):
        # Get the unselectedKeys and selectedCourseIds from query parameters
        unselectedKeys = request.query_params.getlist('unselectedKeys[]')
        selectedCourseIds = request.query_params.getlist('selectedCourseIds[]')
        
        # Query all sections based on selected course ids
        sections = Section.objects.filter(course_id__in=selectedCourseIds)
        
        # Filter out the sections present in unselectedKeys
        sections = sections.exclude(id__in=unselectedKeys)
        
        # Convert sections to a list of dictionaries with necessary information
        section_objects = []
        for section in sections:
            section_data = {
                'id': section.id,
                'course_id': section.course_id,
                'start_time': None,
                'end_time': None,
                'days': [],
                'course_credits': section.course.course_credits
            }
            # Retrieve start and end times from SectionDetails and days from SectionDays
            section_details = section.sectiondetails
            if section_details:
                section_data['start_time'] = section_details.start_time
                section_data['end_time'] = section_details.end_time
            section_data['days'] = [day.day for day in section.sectiondays_set.all()]
            section_objects.append(section_data)
            # Store course ID for the section

        # Join with SectionChain to retrieve alternate start/end times and days
        for section_obj in section_objects:
            section_id = section_obj['id']
            section_chain = SectionChain.objects.filter(section_id=section_id).first()
            if section_chain:
                section_obj['alt_start_time'] = section_chain.alt_start_time
                section_obj['alt_end_time'] = section_chain.alt_end_time
                section_obj['alt_days'] = [day.alt_day for day in section_chain.sectionchaindays_set.all()]

        # Perform credit check on combinations of courses
        LL_credit_hours = 15
        UL_credit_hours = 17

        combinations_list = credit_check(section_objects, LL_credit_hours, UL_credit_hours)

        # Filter combinations that have clashes
        combinations_without_clashes = [combination for combination in combinations_list if not clash_check(combination)]

        # Filter combinations that have duplicate course IDs
        combinations_without_duplicates = [combination for combination in combinations_without_clashes if not has_duplicate_course_id(combination)]

        # Retrieve section_ids from combinations
        section_ids_combinations = [
                                        [section['id'] for section in combination]  # Select the IDs of sections not ending with 'alt' in each combination
                                        for combination in combinations_without_duplicates  # Iterate over combinations
                                    ]

        # Retrieve detailed information for each section_id
        detailed_sections = []
        for section_ids in section_ids_combinations:
            detailed_combination = []
            for section_id in section_ids:
                section = get_detailed_section_info(section_id)
                detailed_combination.append(section)
            detailed_sections.append(detailed_combination)

        return Response({"combinations": detailed_sections})


def credit_check(courses, LL_credit_hours, UL_credit_hours):
    # If there are no courses, return an empty list
    if not courses:
        return []

    # Find the maximum and minimum credit hours among the courses
    max_credit_hours = max(course['course_credits'] for course in courses)
    min_credit_hours = min(course['course_credits'] for course in courses if course['course_credits'] != 0)

    # If the maximum credit hours is 0, handle special cases
    if max_credit_hours == 0:
        # If the lower limit credit hours is also 0, return all combinations of courses
        if LL_credit_hours == 0:
            return [combination for r in range(1, len(courses)+1) for combination in combinations(courses, r)]
        else:
            # Otherwise, there are no valid combinations, return an empty list
            return []

    combinations_list = []

    # Calculate the lower and upper limit number of courses based on credit hours
    LL = max(1, LL_credit_hours // max_credit_hours)
    UL = min(len(courses) + 1, (UL_credit_hours // min_credit_hours) + 1)
                             
    # Iterate over different numbers of courses
    for r in range(LL, UL):
        # Generate combinations of courses for the current number of courses
        for combination in combinations(courses, r):
            total_credit_hours = sum(course['course_credits'] for course in combination)

            # Check if the total credit hours fall within the desired range
            if LL_credit_hours <= total_credit_hours <= UL_credit_hours:
                combinations_list.append(combination)

    return [combination for combination in combinations_list if combination]


def clash_check(courses):
    processed_courses = list(courses)
    additional_courses = []

    for course in processed_courses:
        # Check if the course has alternative timings
        if 'alt_days' in course:
            # Construct a new course entry with alternative timings
            additional_course = {
                'id': course['id'],
                'days': course['alt_days'],
                'start_time': course['alt_start_time'],
                'end_time': course['alt_end_time']
            }
            additional_courses.append(additional_course)

    # Extend the processed courses list with additional courses
    processed_courses.extend(additional_courses)
    
    # Filter out courses with None start times
    processed_courses = [course for course in processed_courses if course['start_time'] is not None]

    # Iterate over courses to check for clashes
    for i in range(len(processed_courses) - 1):
        course1 = processed_courses[i]
        course1_days = set(course1['days'])
        course1_start = course1['start_time']
        course1_end = course1['end_time']

        for j in range(i + 1, len(processed_courses)):
            course2 = processed_courses[j]
            course2_days = set(course2['days'])
            course2_start = course2['start_time']
            course2_end = course2['end_time']

            # Check if the courses have overlapping days and times
            if course1_days.intersection(course2_days):
                if (course1_start <= course2_start <= course1_end) \
                        or (course1_start <= course2_end <= course1_end) \
                        or (course2_start <= course1_start <= course2_end) \
                        or (course2_start <= course1_end <= course2_end):
                    return True

    return False


def has_duplicate_course_id(combination):
    course_ids = set()
    for section_data in combination:
        course_id = section_data['course_id']
        if course_id in course_ids:
            return True
        course_ids.add(course_id)
    return False


def get_detailed_section_info(section_id):
    # Retrieve detailed information for a given section_id
    section = Section.objects.get(id=section_id)
    section_details = SectionDetails.objects.get(section=section)
    section_days = [day.day for day in SectionDays.objects.filter(section=section)]
    
    section_chain = SectionChain.objects.filter(section=section).first()
    alt_days = [day.alt_day for day in SectionChainDays.objects.filter(section_chain=section_chain)] if section_chain else []

    # Retrieve course related information
    course = section.course
    dept = course.dept

    # Retrieve classroom information
    location = section_details.location
    alt_location = section_chain.alt_location if section_chain else None

    # Construct a dictionary with relevant information
    section_info = {
        'section_id': section.section_id,  # Corrected to access section_id from Section model
        'id': section.id,
        'course_id': section.course_id,
        'start_time': section_details.start_time,
        'end_time': section_details.end_time,
        'days': section_days,
        'course_credits': course.course_credits,
        'alt_start_time': section_chain.alt_start_time if section_chain else None,
        'alt_end_time': section_chain.alt_end_time if section_chain else None,
        'alt_days': alt_days,
        'course_name': course.course_name,
        'dept': dept.dept_id,
        'course_code': course.course_code,
        'classroom': location[-4:] if location else None,
        'alternative_classroom': alt_location[-4:] if alt_location else None,
    }

    return section_info

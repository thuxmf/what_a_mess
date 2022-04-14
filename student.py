# -*- coding: utf-8 -*-
"""Class for each student."""


import json
import warnings

from course import *


__all__ = ['Student']


class Student(object):
    def __init__(self,
                 name='',
                 class_name='致理-数01',
                 year='2020',
                 id=''):
        """Initialization function.
        
        Args:
            name:        The name of the student. (default: '')
            class_name:  The class name of the student. (default: '致理-数01')
            year:        The year of the student. (default: '2020')
            id:          The id number of the student. (default: '')
        """
        self._name = name
        self._class_name = class_name
        self._year = year
        self._id = id

        # All courses recorded.
        self._courses = dict()
        # All failed coursed recorded.
        self._failed_courses = dict()

    @property
    def name(self):
        """The name of the student."""
        return self._name

    @property
    def class_name(self):
        """The class name of the student."""
        return self._class_name

    @property
    def year(self):
        """The year of the student."""
        return self._year

    @property
    def id(self):
        """The id number of the student."""
        return self._id

    @property
    def courses(self):
        """The courses recorded of the student."""
        return self._courses

    @property
    def failed_courses(self):
        """The failed courses recorded of the student."""
        return self._failed_courses

    def add_course(self, course: Course):
        """Add a course using a LAZY strategy, i.e., if adding a course with
        the same name as a previous one, overwrite it directly.
        """
        # if course.name in self._courses:
        #     warnings.warn(f'Try to add a course the second time with '
        #                   f'({course.name}, {self._name}).')
        self._courses[course.name] = course
        if course.rank == 'F':
            self._failed_courses[course.name] = course
        return course

    def calc_average_grade(self, type_level, semesters=None):
        """Calculate the average grade of all courses with course type level
        smaller or equal to `type_level`.
        """
        total_grade, total_score = 0.0, 0
        for _, course in self._courses.items():
            level = COURSE_TYPES[course.course_type]
            # Discard if this course not needed.
            if level > type_level:
                continue
            # Discard if this course not in the specified semester.
            if semesters is not None:
                if not semesters[0] <= course.semester <= semesters[1]:
                    continue
            # Discard if this course cannot be calculated.
            if not course.calc_grade_flag():
                continue
            total_grade += course.total_grade
            total_score += course.score
        if total_score == 0:
            return 0, 0.0
        return total_score, total_grade / float(total_score)

    def collect_failed_courses(self, semesters=None):
        failed = []
        print(semesters)
        for _, course in self._failed_courses.items():
            if semesters is not None:
                if not semesters[0] <= course.semester <= semesters[1]:
                    continue
            failed.append(course.info())
        return failed

    def info(self):
        info_dict = {
            'name': self._name,
            'class_name': self._class_name,
            'year': self._year,
            'id': self._id,
            'courses': {k: v.info() for k, v in self._courses.items()},
            'failed_courses': {k: v.info() for k, v in self._failed_courses.items()}
        }
        return info_dict

    def __str__(self):
        return json.dumps(self.info(), indent=4, ensure_ascii=False)

# -*- coding: utf-8 -*-
"""Class for the database."""


from student import Student
from class_names import CLASS_NAMES


class DataBase(dict):
    def __init__(self):
        self._classes = {class_name: [] for class_name in CLASS_NAMES}
        
        # Last reocrd of the average grades.
        self.hot_grades_average = None

    @property
    def classes(self):
        return self._classes

    def add_single_record(self,
                          student: Student,
                          course):
        student_id = student.id
        if student_id in self:
            student = self[student_id]
        student.add_course(course)
        self[student_id] = student

    def update_classes(self):
        self._classes = {class_name: [] for class_name in CLASS_NAMES}
        for _, student in self.items():
            if student.class_name not in CLASS_NAMES:
                raise ValueError(f'Please update `class_names.py` before '
                                 f'updating the database.')
            self._classes[student.class_name].append(student)

    def fetch_student(self, id):
        """Id is the only way allowed to fetch student data directly."""
        return self[id]

    def fetch_class(self, class_name):
        """Class name is the only way allowed to fetch class data directly."""
        return self._classes[class_name]

    def update_average_grade(self, type_level, semesters=None):
        """To avoid returning all records, calculate the average grade class-wise."""
        grades_classwise = {class_name: [] for class_name in CLASS_NAMES}
        for class_name, class_list in self._classes.items():
            for student in class_list:
                average_grade, total_score = student.calc_average_grade(
                    type_level, semesters)
                grades_classwise[class_name].append((
                    student.id, student.name,
                    class_name, total_score, average_grade))
        self.hot_grades_average = grades_classwise
        return grades_classwise

    def collect_failed_courses(self, semesters):
        failed_classwise = {class_name: dict() for class_name in CLASS_NAMES}
        for class_name, class_list in self._classes.items():
            for student in class_list:
                failed_courses = student.collect_failed_courses(semesters)
                if len(failed_courses) == 0:
                    continue
                failed_classwise[class_name][student.name] = failed_courses
        return failed_classwise

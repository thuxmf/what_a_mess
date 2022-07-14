# -*- coding: utf-8 -*-
"""File for all utility functions."""


import pandas as pd


from student import Student
from course import Course


__all__ = [
    'dict2course'
]


COURSE_CH2EN = {
    '课程名': 'name',
    '成绩': 'rank',
    '绩点成绩': 'grade',
    '学分': 'score',
    '课程属性': 'course_type',
    '教师名': 'teacher',
    '学年学期': 'semester'
}

STUDENT_CH2EN = {
    '学号': 'id',
    '姓名': 'name',
    '教学班级': 'class_name',
}


def dict2course(data_dict):
    """Convert one raw record to course and student record."""
    course_dict = dict()
    for ch, en in COURSE_CH2EN.items():
        course_dict[en] = data_dict.pop(ch)
    course = Course(**course_dict)
    assert len(STUDENT_CH2EN) == len(data_dict)
    student_dict = dict(zip(map(lambda k: STUDENT_CH2EN[k], data_dict.keys()), data_dict.values()))
    return student_dict, course
    

def dict2student(student_dict):
    """Convert one raw record to the student record."""
    student_dict['id'] = str(student_dict['id'])
    student_dict['year'] = student_dict['id'][:4]
    return Student(**student_dict)


def convert_semesters(semesters):
    """Convert the raw semester string to an interval one."""
    if semesters.lower() == 'none':
        return None
    semesters = semesters.split(',')
    # A whole year or one single semester
    if len(semesters) == 1:
        semester = semesters[0]
        # A whole year, e.g., '2020-2021'
        if len(semester) == 9:
            semesters = [semester+'-1', semester+'-3']
        # A single semester, e.g., '2020-2021-1'
        elif len(semester) == 11:
            semesters = [semester, semester]
        else:
            raise ValueError(f'Wrong type of semester, only input of the forms'
                             f' `2020-2021-1,2020-2021-2`, `2020-2021` and '
                             f'`2020-2021-1` are allowed.')
        return semesters
    # A complete interval
    elif len(semesters) == 2:
        return semesters
    else:
        raise ValueError(f'Wrong type of semester, only input of the forms'
                         f' `2020-2021-1,2020-2021-2`, `2020-2021` and '
                         f'`2020-2021-1` are allowed.')


def grade2dict(grade_record):
    """Convert one grade record to a dict.
    
    NOTE: The record is expected to be of the form
    (id, name, class_name, score, grade).
    """
    id, name, class_name, score, grade = grade_record
    return dict(
        id=id,
        name=name,
        class_name=class_name,
        score=score,
        grade=grade
    )


def grade2series(grade_record):
    grade_dict = grade2dict(grade_record)
    return pd.Series(grade_dict)


def grades2df(grades):
    grades = [grade2series(x) for x in grades]
    return pd.DataFrame(grades)


def sort(grades, strategy):
    """Sort the grade records in one class, allow three kinds of strategies,
    i.e., grade, id or total grade."""
    if strategy == 'grade':
        cmp = lambda x: x[4]
    elif strategy == 'id':
        cmp = lambda x: x[0]
    elif strategy == 'total':
        cmp = lambda x: x[3] * x[4]
    else:
        raise NotImplementedError(f'Wrong type of strategy. Only allow to sort '
                                  f'grade, id or total.')
    for class_name, grade in grades.items():
        grades[class_name] = sorted(grade, key=cmp, reverse=(strategy != 'id'))

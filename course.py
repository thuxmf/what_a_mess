# -*- coding: utf-8 -*-
"""Class to record each course."""


import json

__all__ = [
    'Course',
    'COURSE_TYPES',
    'BIXIU',
    'XIANXUAN',
    'RENXUAN'
]

BIXIU = 0  # 必修
XIANXUAN = 1  # 限选
RENXUAN = 2  # 任选

COURSE_TYPES = {
    '必修': BIXIU,
    '限选': XIANXUAN,
    '任选': RENXUAN,
}


class Course(object):
    def __init__(self,
                 name='',
                 rank='A',
                 grade=0.0,
                 score=0,
                 course_type='必修',
                 teacher='',
                 semester=''):
        """Initialization function.
        
        Args:
            name:         The name of the course. (default: '')
            rank:         The rank of the course. (default: 'A')
            grade:        The grade of the course. (default: 0.0)
            score:        The score of the course. (default: 0)
            course_type:  The type of the course. (default: '必修')
            teacher:      The teacher of the course. (default: '')
            semester:     The semester of the course. (default: '')
        """
        self._name = name
        self._rank = rank
        # Rank 'F' will get a N/A.
        if not 0.0 <= grade <= 4.0:
            self._grade = 0.0
        else:
            try:
                self._grade = float(grade)
            except ValueError:
                self._grade = 0.0
        self._score = int(score)
        self._course_type = course_type
        self._teacher = teacher
        self._semester = semester

        if course_type not in COURSE_TYPES:
            raise ValueError(f'Received wrong course type {course_type}, which'
                             f' should be one of {COURSE_TYPES}')

    @property
    def name(self):
        """The name of the course."""
        return self._name

    @property
    def rank(self):
        """The rank of the course, e.g., A+, B-."""
        return self._rank

    @property
    def grade(self):
        """The grade of the course, e.g., 4.0, 3.6."""
        return self._grade

    @property
    def score(self):
        """The score of the course, i.e., 2, 3."""
        return self._score
    @property
    def course_type(self):
        """The course type of the course, i.e., 必修, 任选."""
        return self._course_type

    @property
    def teacher(self):
        """The name of the teacher of the course."""
        return self._teacher

    @property
    def semester(self):
        """The semester of the course."""
        return self._semester

    @property
    def total_grade(self):
        """The total grade of a course, by `grade` * `score`."""
        return self._grade * float(self._score)

    def calc_grade_flag(self):
        """If the rank of a course is W, I or P, it will not be calculated."""
        return self._rank not in ['W', 'I', 'P', 'EX']

    def info(self):
        info_dict = {
            'name': self._name,
            'rank': self._rank,
            'grade': self._grade,
            'score': self._score,
            'course_type': self._course_type,
            'teacher': self._teacher,
            'semester': self._semester,
            'calc_grade_flag': self.calc_grade_flag()
        }
        return info_dict

    def __str__(self):
        return json.dumps(self.info(), indent=4, ensure_ascii=False)

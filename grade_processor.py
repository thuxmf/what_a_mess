# -*- coding: utf-8 -*-
"""Main file to process grades."""


import os
import json

import click
import numpy as np
from tqdm import tqdm

from database import DataBase
from class_names import CLASS_NAMES
from course import *
from utils.utils import dict2course, dict2student
from utils.utils import convert_semesters, grades2df, sort
from utils.xls_processor import XLSXProcessor


@click.command(help='Update the database using grades of the new semester.',
    context_settings={'show_default': True, 'max_content_width': 180})
@click.option('--raw_data_path', default='1.xls', type=str, metavar='str',
    help='Path to raw data downloaded directly from the info.tsinghua.edu.cn.')
@click.option('--database_path', default='database.npy', type=str,
    metavar='str', help='Path to the previous database file or where to save.')
@click.option('--index', default=0, type=int, metavar='int',
    help='Which sheet to load, by default 0 since there is only 1 sheet.')
@click.option('--header', default=0, type=int, metavar='int',
    help='Whether to load the header, by default 0 since there is header.')
def update(raw_data_path, database_path, index, header):
    if database_path is not None and os.path.exists(database_path):
        database = np.load(database_path, allow_pickle=True).item()
    else:
        database = DataBase()
    data = XLSXProcessor.fetch_data(raw_data_path, index, header)
    for _, data_dict in tqdm(data.items(), total=len(data)):
        student_dict, course = dict2course(data_dict)
        student = dict2student(student_dict)
        database.add_single_record(student, course)
    database.update_classes()
    np.save(database_path, database)
    print(f'During update: # Record: {len(data)}, # Student: {len(database)}.')


@click.command(help='Calculate the average grades classwise by different strategies.',
    context_settings={'show_default': True, 'max_content_width': 180})
@click.option('--database_path', default='database.npy', type=str,
    metavar='str', help='Path to the previous database file.')
@click.option('--type_level', default=XIANXUAN, metavar='int', type=int,
    help=f'At which level to calculate the average grade, BIXIU=0, XIANXUAN=1 '
         f'and RENXUAN=2. All courses with level SMALLER or EQUAL to the given'
         f' level will be calculated.')
@click.option('--semesters', default='2020-2021-1,2020-2021-2', type=str,
    metavar='str',
    help=f'During which semester the courses will be included. Three kinds of '
         f'inputs are allowed, i.e., `2020-2021-1,2021-2022-2`, or `2020-2021`'
         f' or `2021-2022-2`.')
@click.option('--save_path', default='average_grades.xls', type=str,
    metavar='str', help='Path to save the output file.')
@click.option('--strategy', default='grade',
    type=click.Choice(['id', 'grade', 'total']),
    help='By which strategy to sort the grade records, id, grade or total grades.')
def calculate(database_path, type_level, semesters, save_path, strategy):
    database = np.load(database_path, allow_pickle=True).item()
    semesters = convert_semesters(semesters)
    average_grades = database.update_average_grade(type_level, semesters)
    sort(average_grades, strategy)
    print(average_grades)
    dfs = [grades2df(grades) for grades in average_grades.values()]
    XLSXProcessor.save(save_path, dfs, CLASS_NAMES)


@click.command(help='Collect all failed courses.',
    context_settings={'show_default': True, 'max_content_width': 180})
@click.option('--database_path', default='database.npy', type=str,
    metavar='str', help='Path to the previous database file.')
@click.option('--semesters', default='2020-2021-1,2020-2021-2', type=str,
    metavar='str',
    help=f'During which semester the courses will be included. Three kinds of '
         f'inputs are allowed, i.e., `2020-2021-1,2021-2022-2`, or `2020-2021`'
         f' or `2021-2022-2`.')
@click.option('--save_path', default='failed_courses.txt', type=str,
    metavar='str', help='Path to save the output file.')
def failed(database_path, semesters, save_path):
    database = np.load(database_path, allow_pickle=True).item()
    semesters = convert_semesters(semesters)
    failed_courses = database.collect_failed_courses(semesters)
    with open(save_path, 'w') as fp:
        json.dump(failed_courses, fp, indent=4, ensure_ascii=False)


@click.group(name='The processor to process grades.',
    context_settings={'show_default': True, 'max_content_width': 180})
def command_group():
    pass


@command_group.result_callback()
@click.pass_context
def main(ctx, kwargs):
    invoked_subcommand = ctx.invoked_subcommand
    print(f'executing `main` through `{invoked_subcommand}`')


if __name__ == '__main__':
    command_group.add_command(update)
    command_group.add_command(calculate)
    command_group.add_command(failed)
    command_group()

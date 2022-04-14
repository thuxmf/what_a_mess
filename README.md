# 扶倒猿批量操作的各种代码

如有任何bug或建议请邮件联系<xmf20@mails.tsinghua.edu.cn>

## 成绩处理

在[信息门户](info.tsinghua.edu.cn)导出成绩时只勾选如下八条，便于后续批量操作：

1. 学号
2. 姓名
3. 教学班级
4. 课程名
5. 成绩
6. 绩点成绩
7. 学年学期
8. 学分
9. 课程属性
10. 教师名

下载后在[class_names.py](class_names.py)中相应地修改修改班级列表以及`CLASS_NAMES`

`grade_processor.py`提供三种功能，分别为**更新数据库**，**计算平均绩**和**统计挂科情况**

### 更新数据库

命令的参数介绍如下：

```shell
Usage: grade_processor.py update [OPTIONS]

  Update the database using grades of the new semester.

Options:
  --raw_data_path str  Path to raw data downloaded directly from the info.tsinghua.edu.cn.  [default: 1.xls]
  --database_path str  Path to the previous database file or where to save.  [default: database.npy]
  --index int          Which sheet to load, by default 0 since there is only 1 sheet.  [default: 0]
  --header int         Whether to load the header, by default 0 since there is header.  [default: 0]
  --help               Show this message and exit.  [default: False]
```

因此可以使用

```shell
python grade_processor.py update --raw_data_path path/to/file/downloaded/from/info.xls
```

### 计算平均绩

命令的参数介绍如下：

```shell
Usage: grade_processor.py calculate [OPTIONS]

  Calculate the average grades classwise by different strategies.

Options:
  --database_path str          Path to the previous database file.  [default: database.npy]
  --type_level int             At which level to calculate the average grade, BIXIU=0, XIANXUAN=1 and RENXUAN=2. All courses with level SMALLER or EQUAL to the given level will be calculated.  [default: 1]
  --semesters str              During which semester the courses will be included. Three kinds of inputs are allowed, i.e., `2020-2021-1,2021-2022-2`, or `2020-2021` or `2021-2022-2`.  [default: 2020-2021-1,2020-2021-2]
  --save_path str              Path to save the output file.  [default: average_grades.xls]
  --strategy [id|grade|total]  By which strategy to sort the grade records, id, grade or total grades.  [default: grade]
  --help                       Show this message and exit.  [default: False]
```

设置`--type_level`可以选择计算哪些课程的成绩，0为只计算必修，1为必限，2为全部

设置`--semesters`可以选择成绩计算区间，这里共有四种设置方式：
1. `2020-2021-1,2021-2022-2`代表2020-2021学年秋季学期（含）到2021-2022春季学期（含）。（注意`2021-2022-3`代表夏季学期）
2. `2020-2021`代表整个2020-2021学年
3. `2020-2021-2`代表只计算2020-2021春季学期成绩
4. `none`代表所有学期的成绩

设置`--strategy`可以选择排序策略，这里共有三种设置方式：
1. `id`代表按学号从小到大
2. `grade`代表平均绩点从高到低
3. `total`代表总绩点从高到低

因此可以使用

```shell
python grade_processor.py calculate --database_path path/to/your/database.npy --semesters 2020-2021 --strategy grade
```

即可得到按照**教学班级**划分的平均绩点

### 统计挂科情况

命令的参数介绍如下：

```shell
Usage: grade_processor.py failed [OPTIONS]

  Collect all failed courses.

Options:
  --database_path str  Path to the previous database file.  [default: database.npy]
  --semesters str      During which semester the courses will be included. Three kinds of inputs are allowed, i.e., `2020-2021-1,2021-2022-2`, or `2020-2021` or `2021-2022-2`.  [default: 2020-2021-1,2020-2021-2]
  --save_path str      Path to save the output file.  [default: failed_courses.txt]
  --help               Show this message and exit.  [default: False]
```

`--semesters`参数同之前一致，结果会以`txt`形式保存

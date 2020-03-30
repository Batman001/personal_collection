# -*- coding:utf-8 -*-
import os
import datetime
import calendar
import codecs
import sys


def init_month():
    """
    生成当月的年份、月份、最后一天日期、当月每周包含的日期列表
    :return:
    """
    now = datetime.datetime.now()
    curr_year = now.year
    curr_month = now.month if now.month < 10 else int("0" + str(now.month))

    weekday, last_day = calendar.monthrange(curr_year, curr_month)
    # 得出这个月所有的星期天是几号
    sundays = [x for x in range(6 - weekday + 1, last_day + 1, 7)]
    # 得出每周包含的日期数
    week_days = cut(range(1, last_day + 1), sundays)
    return curr_year, curr_month, last_day, week_days


def generate_day_file(curr_year, curr_month, last_day,):
    """
    每天生成当月文件夹结构及其README.md文档
    :param curr_year: 当年年份
    :param curr_month: 当月月份
    :param last_day: 当月最大日期数
    :return:
    """
    days = [_ for _ in range(1, last_day + 1)]
    days = process_folder_sort(days)
    for day in days:
        current_file_path = str(curr_month) + "月" + "/" + str(curr_month) + "." + day + "日"
        os.makedirs(current_file_path)
        f = codecs.open(current_file_path + "/" + "README.md", "w")

        f.write("## " + str(curr_year) + "年" + "/" + str(curr_month) + "月" + "/" + str(day) + " 日报")
        f.close()
    print("Daily Folders Generated!")


def generate_week_file(curr_year, curr_month, week_days):
    """
    每周生成当月的文件夹结构及其README.md文档
    :param curr_year: 当年年份
    :param curr_month: 当月月份
    :param week_days: 当月每周包含的日期列表
    :return:
    """
    weeks = [_ for _ in range(1, len(week_days) + 1)]
    weeks = process_folder_sort(weeks)
    # 生成每月的周报文件夹
    for i in range(len(weeks)):
        current_week = [str(item) for item in list(week_days[i])]
        curr_week_path = str(curr_month) + "月/" + "第" + weeks[i] + "周" + "(" + str(curr_month) + "." + current_week[0] \
            + "-" + str(curr_month) + "." + current_week[-1] + ")"
        os.makedirs(curr_week_path)
        # 同时生成每周的周报的说明文档,文档中包含该周包含的日期
        f = codecs.open(curr_week_path + "/" + "README.md", "w")

        f.write("## " + str(curr_year) + u"年" + str(curr_month) + u"月" + u"第" + str(i + 1) + u"周报" + "\t\n")
        f.write("```" + "\n" + str(calendar.month(curr_year, curr_month)) + "\n" + "```")
        f.write("\n")
        f.write(">" +  u"周报包含日期为: " + "、".join(current_week))
        f.close()

    print("Weekly Folders Generated!")
    

def process_folder_sort(folders):
    """
    保证生成的文件夹按照从小到大进行索引排序
    :param folders:
    :return:
    """
    folders_ = []
    for item in folders:
        if 0 < item < 10:
            item = "0" + str(item)
        folders_.append(str(item))
    return folders_


def cut(arr, indices):
    """
    #把一个列表按下标切分
    :param arr:
    :param indices:
    :return:
    """
    return [arr[i:j] for i, j in zip([0]+indices, indices+[None])]


def run():
    """
    生成当月日报或者周报文件夹的执行程序入口函数
    :return:
    """
    curr_year, curr_month, last_day, week_days = init_month()
    while True:
        try:
            user_input = input("Weekly or Daily? If Daily input -d else input -w ! ")
            if user_input == "-w":
                generate_week_file(curr_year, curr_month, week_days)
                break
            elif user_input == "-d":
                generate_day_file(curr_year, curr_month, last_day)
                break
            else:
                raise NameError
        except NameError:
            print("输入选项错误,请重新输入!")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("输入参数错误!必须存在生成目录路径,请输入生成目录的路径!")
        sys.exit(0)
    target_location = sys.argv[1]
    os.chdir(target_location)
    run()


"""
* Copyright (c) BillDa
* https://www.youtube.com/channel/UCsmrG8l2cZIa6EeJJEqrFQA
"""
from datetime import datetime

"""
date
six number array
strong number
number of winner of lotto
number of winner of double-lotto hjjkj
"""


class LDB:
    res_count = 0
    win_count = 0
    dbwin_count = 0

    def __init__(self, lotto_num, date, six_num_arr, x_num, win_num, dbwin_num):
        self.lotto_num = lotto_num
        self.date = date
        self.six_num_arr = six_num_arr
        self.x_num = x_num
        self.win_num = win_num
        self.dbwin_num = dbwin_num

    def __add__(self, lotto_num, date, six_num_arr, x_num, win_num, dbwin_num):
        self.lotto_num = lotto_num
        self.date = date
        self.six_num_arr = six_num_arr
        self.x_num = x_num
        self.win_num = win_num
        self.dbwin_num = dbwin_num

    def __bool__(self):
        return self.res_count > 0

    def print_ldb(self):
        print(self.date, self.six_num_arr, self.x_num, self.win_num, self.dbwin_num)

def srt_to_date (str_date):

    str_date_obj = datetime.strptime(str_date, '%d/%m/%y').date()
    return str_date_obj
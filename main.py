import datetime
from tkinter import *
import requests
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import ldb

global file_name
global ldb_list
global res_lst_ticket

global root
global strongNums
global couples
global chain_num
global numsOnlyWins
function_counter = 0


def tests():
    submit_ldb()
    a = [5, 5]
    randomBySeed(a)
    graphs()

    # wining_dates()

    # counter = 0
    # winer_counter = 0
    # for temp1 in ldb_list:
    #     if temp1.lotto_num < 1841:
    #         break
    #     for temp2 in ldb_list:
    #         if temp2.lotto_num < 1841:
    #             break
    #         if temp1.lotto_num != temp2.lotto_num:
    #             if temp1.six_num_arr[0] == temp2.six_num_arr[0]:
    #                 if temp1.six_num_arr[1] == temp2.six_num_arr[1]:
    #                     if temp1.six_num_arr[2] == temp2.six_num_arr[2]:
    #                         if temp1.six_num_arr[3] == temp2.six_num_arr[3]:
    #                             counter += 1
    #                             if temp1.six_num_arr[4] == temp2.six_num_arr[4]:
    #                                 print("Bill")
    #                                 if temp1.six_num_arr[5] == temp2.six_num_arr[5]:
    #                                     counter += 1
    #                                     if temp1.win_num > 0 or temp1.dbwin_num > 0:
    #                                         winer_counter += 1
    # print(counter)
    # print(winer_counter)


def strongNums():
    """
    function getting the best numbers
    :return: List the 6 number & extra (7 numbers in total)
    """
    # Part1 - making data list
    num_list = np.zeros((38,), dtype=int)
    st_num_list = np.zeros((8,), dtype=int)
    for item in ldb_list:
        for num in item.six_num_arr:
            num_list[num] += 1
        if item.x_num < 8:
            st_num_list[item.x_num] += 1

    # part2 - making result list
    max_strong_index1 = list(st_num_list).index(max(st_num_list))            # Getting strong num
    temp_st = st_num_list[max_strong_index1]
    st_num_list[max_strong_index1] = 0
    max_strong_index2 = list(st_num_list).index(max(st_num_list))  # Getting strong num
    st_num_list[max_strong_index1] = temp_st

    result_list = np.zeros((12,), dtype=int)
    result_list_i = np.zeros((12,), dtype=int)
    for i in range(0, 12):                                                    # Getting 12 number
        result_list[i] = max(num_list)
        result_list_i[i] = list(num_list).index(result_list[i])
        num_list[result_list_i[i]] = 0

    res_list = []
    for i in range(0, 12):
        num_list[result_list_i[i]] = result_list[i]
        res_list.append(result_list_i[i])
    res_list.append(max_strong_index1)
    res_list.append(max_strong_index2)

    return res_list, num_list, st_num_list


def strongNumsOnlyWins():
    """
    function getting the best numbers only from wins
    :return: List the 6 number & extra (7 numbers in total)
    """
    num_list = np.zeros((38,), dtype=int)
    st_num_list = np.zeros((8,), dtype=int)
    for item in ldb_list:
        if item.win_num > 0 or item.dbwin_num > 0:
            for num in item.six_num_arr:
                num_list[num] += 1
            if item.x_num < 8:
                st_num_list[item.x_num] += 1

    # part2 - making result list
    max_strong_index1 = list(st_num_list).index(max(st_num_list))            # Getting strong num
    st_num_list[max_strong_index1] = 0
    max_strong_index2 = list(st_num_list).index(max(st_num_list))            # Getting strong num

    result_list = np.zeros((12,), dtype=int)
    result_list_i = np.zeros((12,), dtype=int)
    for i in range(0, 12):
        result_list[i] = max(num_list)
        result_list_i[i] = list(num_list).index(result_list[i])
        num_list[result_list_i[i]] = 0

    res_list = []
    for i in range(0, 12):
        num_list[result_list_i[i]] = result_list[i]
        res_list.append(result_list_i[i])
    res_list.append(max_strong_index1)
    res_list.append(max_strong_index2)

    return res_list, num_list


def couples():
    """
    function getting the best numbers only from wins
    :return: List the 6 number & extra (7 numbers in total)
    """
    num_list = np.zeros((38, 38), dtype=int)
    st_num_list = np.zeros((8,), dtype=int)
    for item in ldb_list:
        for a in item.six_num_arr:
            for b in item.six_num_arr:
                if a != b:
                    num_list[int(a)][int(b)] += 1

    temp_num_list = num_list.copy()
    max_num_list = []
    max_index_list = []
    while len(max_num_list) < 6:
        max_num = 0
        row_m = 0
        cul_m = 0
        for row in range(0, 38):
            for cul in range(0, 38):
                if cul > row:
                    if temp_num_list[row][cul] > max_num:
                        max_num = temp_num_list[row][cul]
                        row_m = row
                        cul_m = cul
        max_num_list.append(max_num)
        max_index_list.append(row_m)
        max_index_list.append(cul_m)
        for row in range(0,38):
            for cul in range(0, 38):
                if row == row_m or cul == cul_m:
                    temp_num_list[row][cul] = 0

    for item in ldb_list:
        for num in item.six_num_arr:
            if num in max_index_list:
                st_num_list[item.x_num] += 1
                break
    max_strong_index1 = list(st_num_list).index(max(st_num_list))  # Getting strong num
    st_num_list[max_strong_index1] = 0
    max_strong_index2 = list(st_num_list).index(max(st_num_list))  # Getting strong num
    max_index_list.append(max_strong_index1)
    max_index_list.append(max_strong_index2)

    return max_index_list, num_list


def wining_dates():
    """
    function getting the best date to fill ticket
    :return: TODO: BILL wining_dates
    """
    wining_list = []
    # Add only wining from DB
    for item in ldb_list:
        if item.win_num > 0 or item.dbwin_num > 0:
            wining_list.append(item)

    print(len(wining_list))


def chain_num():
    """
    download csv from lotto website
    :return: List the 6 number & extra (7 numbers in total)
    """
    num_list_counter = np.zeros((38,), dtype=int)   # number of shows in a row
    many_list_chain = np.zeros((38,), dtype=int)
    num_list_max = np.zeros((38,), dtype=int)
    st_num_counter = np.zeros((8,), dtype=int)
    st_num_chain = np.zeros((8,), dtype=int)
    st_num_max = np.zeros((8,), dtype=int)

    temp_six_arr = [ldb_list[0].six_num_arr[0], ldb_list[0].six_num_arr[1], ldb_list[0].six_num_arr[2],
                    ldb_list[0].six_num_arr[3], ldb_list[0].six_num_arr[4], ldb_list[0].six_num_arr[5]]
    temp_x_num = ldb_list[0].x_num
    for item in ldb_list:
        if item.lotto_num < 1841:                                           # Breaking point
            break
        for temp in item.six_num_arr:                                       # 6 num chain
            num_list_counter[temp] += 1
            if num_list_counter[temp] == 3:
                many_list_chain[temp] += 1
            if num_list_counter[temp] > num_list_max[temp]:
                num_list_max[temp] = num_list_counter[temp]
        for old_temp in temp_six_arr:
            if old_temp in item.six_num_arr:
                continue
            num_list_counter[old_temp] = 0
        temp_six_arr = [item.six_num_arr[0], item.six_num_arr[1], item.six_num_arr[2],
                        item.six_num_arr[3], item.six_num_arr[4], item.six_num_arr[5]]

        st_num_counter[item.x_num] += 1                                        # x_num chain
        st_num_chain[item.x_num] += 1
        if st_num_counter[item.x_num] > st_num_max[item.x_num]:
            st_num_max[item.x_num] = st_num_counter[item.x_num]
        if temp_x_num != item.x_num:
            temp_x_num = item.x_num
            st_num_counter[item.x_num] = 0

    # part2 - making result list
    num_list_counter = np.zeros((38,), dtype=int)
    for i in range(0, 38):
        num_list_counter[i] = num_list_max[i]*2 + many_list_chain[i]
    for i in range(0, 8):
        st_num_counter[i] = st_num_chain[i] + st_num_max[i] * 3

    result_list = np.zeros((12,), dtype=int)
    result_list_i = np.zeros((12,), dtype=int)
    for i in range(0, 12):
        result_list[i] = max(num_list_counter)
        result_list_i[i] = list(num_list_counter).index(result_list[i])
        num_list_counter[result_list_i[i]] = 0

    res_list = []
    for i in range(0, 12):
        num_list_counter[result_list_i[i]] = result_list[i]
        res_list.append(result_list_i[i])
    temp_x_num = list(st_num_counter).index(max(st_num_counter))
    res_list.append(temp_x_num)
    st_num_counter[temp_x_num] = 0
    res_list.append(list(st_num_counter).index(max(st_num_counter)))
    # print(res_list)
    # print(num_list_max)
    # number of time the num were 3 time in a row
    # print(many_list_chain)

    return res_list, num_list_counter

def randomBySeed(vef_num_list):
    """
    download csv from loto website
    :return: List the 6 number & extra (7 numbers in total)
    """
    random_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                   28, 29, 30, 31, 32, 33, 34, 35, 36, 37] + vef_num_list
    res_list = []
    index = 0
    while len(res_list) < 12:
        index = np.random.choice(random_list)
        res_list.append(index)
        random_list = list(filter(lambda a: a != index, random_list))
    res_list.append(np.random.choice([1, 2, 3, 4, 5, 6, 7]))
    res_list.append(np.random.choice([1, 2, 3, 4, 5, 6, 7]))

    return res_list


def randomByStrongNum():
    """
    download csv from loto website
    :return: List the 6 number & extra (7 numbers in total)
    """
    arr_st_num, num_list, st_num_list = strongNums()
    temp_res_list1 = []
    flag = 0
    while flag != 37:
        for i in range(0,38,1):
            if num_list[i] > 0:
                temp_res_list1.append(i)
                num_list[i] -= 1
                if num_list[i] == 0:
                    flag+=1

    flag = 0
    temp_res_list2 = []
    while flag != 7:
        for i in range(0,8,1):
            if st_num_list[i] > 0:
                temp_res_list2.append(i)
                st_num_list[i] -= 1
                if st_num_list[i] == 0:
                    flag+=1

    res_list = []
    # res_list = np.random.choice(num_list, size=(6))
    index = 0
    while len(res_list) < 12:
        index = np.random.choice(temp_res_list1)
        res_list.append(index)
        temp_res_list1 = list(filter(lambda a: a != index, temp_res_list1))

    index = np.random.choice(temp_res_list2)
    res_list.append(index)
    temp_res_list2 = list(filter(lambda a: a != index, temp_res_list2))
    index = np.random.choice(temp_res_list2)
    res_list.append(index)

    return res_list


def download_lotto_res():
    """
    download csv from loto website
    :return: Flag Bool, True if the file was download successful, False else.
    """
    file_name = "Lotto.csv"
    url1 = 'https://www.pais.co.il/lotto/lotto_resultsDownload.aspx'
    flag = True
    try:
        page_data = requests.get(url1, allow_redirects=True)
        try:
            open(file_name, 'wb').write(page_data.content)
        except:
            flag = False
            print("error writing page_data in to file")
    except:
        flag = False
        print("error get page_data from url")
    finally:
        return flag


# Database

def submit_sql():
    """
    creating sql database
    :return: none
    """
    # create DB
    ldb = sqlite3.connect('ldb.db')
    curs = ldb.cursor()

    # Create table (need do to 1 time)
    # curs.execute("""CREATE TABLE lottoObj (
    #                 lotto_num integer,
    #                 date text,
    #                 num1 integer,
    #                 num2 integer,
    #                 num3 integer,
    #                 num4 integer,
    #                 num5 integer,
    #                 num6 integer,
    #                 strong integer,
    #                 wins integer,
    #                 dawns integer
    #                 )""")

    f = open(file_name, "rb")                                               # Open the csv file
    f.readline()
    count = 0
    count += 1
    for a1 in f:
        lotto_num = int(a1.decode('ascii').rsplit(",")[0])                  # Lotto number
        date = a1.decode('ascii').rsplit(",")[1]                            # Date
        num1 = int(a1.decode('ascii').rsplit(",")[2])                       # First number
        num2 = int(a1.decode('ascii').rsplit(",")[3])                       # Second number
        num3 = int(a1.decode('ascii').rsplit(",")[4])                       # 3 number
        num4 = int(a1.decode('ascii').rsplit(",")[5])                       # 4 number
        num5 = int(a1.decode('ascii').rsplit(",")[6])                       # 5 number
        num6 = int(a1.decode('ascii').rsplit(",")[7])                       # 6 number
        strong = int(a1.decode('ascii').rsplit(",")[8])                     # Extra number
        if lotto_num > 1465:                                                # From here the lotto changes
            wins = int(a1.decode('ascii').rsplit(",")[9])                   # How many wins (Lotto)
        else:
            wins = -1
        if lotto_num > 1841:                                                # Stop collecting data
            dawns = int(a1.decode('ascii').rsplit(",")[10])                 # How many wins (Double-Lotto)
        else:
            break

        # insert the var to table
        ldb.execute(
            "INSET INTO lottoObj VALUES (:lotto_num, :date, :num1, :num2, :num3, :num4, :num5, :num6, :strong, :wins, "
            ":dawns)",
            {
                'lotto_num': lotto_num,
                'date': date,
                'num1': num1,
                'num2': num2,
                'num3': num3,
                'num4': num4,
                'num5': num5,
                'num6': num6,
                'strong': strong,
                'wins': wins,
                'dawns': dawns
            })

        ldb.commit()

    ldb.close()


def submit_ldb():
    """
    creating database from LDB
    :return: none
    """
    #TODO add try 2 func
    f = open(file_name, "rb")                                               # Open the csv file
    f.readline()
    count = 0
    for a1 in f:
        count += 1
        lotto_num = int(a1.decode('ascii').rsplit(",")[0])                  # Lotto number
        date = a1.decode('ascii').rsplit(",")[1]                            # Date
        num1 = int(a1.decode('ascii').rsplit(",")[2])                       # First number
        num2 = int(a1.decode('ascii').rsplit(",")[3])                       # Second number
        num3 = int(a1.decode('ascii').rsplit(",")[4])                       # 3 number
        num4 = int(a1.decode('ascii').rsplit(",")[5])                       # 4 number
        num5 = int(a1.decode('ascii').rsplit(",")[6])                       # 5 number
        num6 = int(a1.decode('ascii').rsplit(",")[7])                       # 6 number
        strong = int(a1.decode('ascii').rsplit(",")[8])                     # Extra number
        if lotto_num > 1465:                                                # From here the lotto changes
            wins = int(a1.decode('ascii').rsplit(",")[9])                   # How many wins (Lotto)
        else:
            wins = -1
        if lotto_num > 2233:                                                # Stop collecting data
            dawns = int(a1.decode('ascii').rsplit(",")[10])                 # How many wins (Double-Lotto)
        else:
            break
        ldb_list.append(ldb.LDB(lotto_num, date, (num1, num2, num3, num4, num5, num6),
                                strong, wins, dawns))

    f.close()


"""
GUI Shit stuff
"""


def graphs(graph_num):
    """
    gui, start menu
    :return: none
    """
    h = strongNums()
    plt.hist(h, 200)
    plt.show()

    # print(num_list)
    # print(st_num_list)
    # x = range(0,38)
    # plt.title("Line graph")
    # plt.ylabel('Y axis')
    # plt.xlabel('X axis')
    # plt.plot(x, num_list, color="red")
    # plt.show()


def start_button():
    global function_counter                                                 # How many functions selected
    # popup("BillDa", "you have to be over 18 for buying lotto ticket")
    submit_ldb()
    if strongNums.get():
        function_counter += 2
    if numsOnlyWins.get():
        function_counter += 2
    if couples.get():
        function_counter += 2
    if chain_num.get():
        function_counter += 2
    if randomByStrongNum.get():
        function_counter += 2
    if randomNum.get():
        function_counter += 2


    ticket_top()


def optionClicked(value):
    myLabel = Label(root, text=value).grid(row=15, column=0)


# messagebox options: showinfo, showwarning, showerror, askquestion, askokcancel, askyesno
def popup(title, info):
    messagebox.showinfo(title, info)


def ticket_top():
    """
    gui, start menu
    :return: none
    """
    top1 = Toplevel()
    top1.title("Lotto Ticket")                                              # Title
    top1.config(bg='#146356')
    font = ('Purisa', 15, 'bold italic')                                    # Font for all
    Label(top1, text="", bg='#146356', fg="white").pack()
    Label(top1, text="Hello and Good Luck!!!",bg='#146356',fg="white").pack()

    my_canvas = Canvas(top1, width=375, height=580, bg='#146356')           # Create the canvas for the ticket
    my_canvas.create_rectangle(268, 0, 272, 580, fill="black")              # Rectangle that create a black line
    x1_start = 30                                                           # Start point for oval (x1,y1,x2,y2)
    y1_start = 15
    x2_start = 60
    y2_start = 45
    btn_grph_list = []
    btn_win_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "A1", "A2", "As"]
    for row in range(0, function_counter):
        my_canvas.create_text(x1_start - 15, y1_start + 15 + (row * 40), fill="black", font=font, text=row + 1)
        for col in range(0, 6):
            my_canvas.create_oval(x1_start + (col * 40), y1_start + (row * 40), x2_start + (col * 40), y2_start + (row * 40), fill="#F90716")
            my_canvas.create_text(x1_start + 15 + (col * 40), y1_start + 15, fill="black", font=font, text="33")
        # Strong number
        my_canvas.create_oval(250 + x1_start, y1_start + (row * 40), 250 + x2_start, y2_start + (row * 40), fill="red")
        my_canvas.create_text(265 + x1_start, y1_start + 15 + (row * 40), fill="black", font=font, text="6")
        # Graph button
        # btn_grph_list.append(Button(my_canvas, text=btn_win_list[row], command=lambda: graphs(row)))
        # btn_grph_list[row].configure(width=5, activebackground="green", relief=FLAT)
        # # btn_win_list.append(my_canvas.create_window(320, y1_start + (row * 40), anchor=NW, window=btn_grph_list[row]))
        # my_canvas.create_window(320, y1_start + (row * 40), anchor=NW, window=btn_grph_list[row])

    # coun = 0
    # for btn in btn_grph_list:
    #     my_canvas.create_window(320, y1_start + (coun * 40), anchor=NW, window=btn)
    #     coun += 1

    button1 = Button(my_canvas, text="A", command=lambda: graphs(0), anchor=W)
    button1.configure(width=5, activebackground="#33B5E5", relief=FLAT)

    button2 = Button(my_canvas, text="B", command=lambda: graphs(1), anchor=W)
    button2.configure(width=5, activebackground="#33B5E5", relief=FLAT)

    my_canvas.create_window(320, 15, anchor=NW, window=button1)
    my_canvas.create_window(320, 55, anchor=NW, window=button2)

    my_canvas.pack(padx=5, pady=5)
    Button(top1, text="End", command=root.quit, fg="black", bg='#7CD1B8').pack()



def gui():
    """
    Main window (GUI), start menu
    :return: none
    """
    global strongNums
    global numsOnlyWins
    global couples
    global chain_num
    global randomByStrongNum
    global randomNum
    global root

    result_list = []
    root = Tk()                                                             # Configure main window
    strongNums = IntVar()
    couples = IntVar()
    chain_num = IntVar()
    numsOnlyWins = IntVar()
    randomByStrongNum = IntVar()
    randomNum = IntVar()

    root.minsize(500, 600)
    root.title("Lotto App")
    root.config(bg='#3E8E7E')
    Label(root, text="", bg='#3E8E7E').pack()                                           # For space between things
    big_font = ('Purisa', 15, 'bold italic')
    frame_font = ('Purisa', 11, 'bold italic')
    small_font = ('Purisa', 11)

    # Configure start menu
    option_download = IntVar()

    Button(root, text="Start", command=start_button,
           fg='#041C32', bg='#7CD1B8', font=big_font).pack(anchor=N)                    # Start button, create ticket
    Label(root, text="", bg='#3E8E7E').pack()                                           # For space between things

    frame = LabelFrame(root, padx=5, pady=0, bg='#3E8E7E',)
    frame.pack(anchor=NW)
    Label(frame, text="Functions to create lotto ticket each one will create 2 rows            "       
                      "                                                                        ",
          bg='#3E8E7E').pack(anchor=NW)                                                 # Set the size of the frame
    Label(frame, text="", bg='#3E8E7E').pack()                                           # For space between things
    Checkbutton(frame, text="Numbers with most appearance in lottery", variable=strongNums, onvalue=True, offvalue=False,
                bg='#3E8E7E', activebackground="#3E8E7E", font=frame_font).pack(anchor=NW)
    Checkbutton(frame, text="Numbers with most appearance in lottery (Only wining tickets)", variable=numsOnlyWins,
                onvalue=True, offvalue=False, activebackground="#3E8E7E", bg='#3E8E7E', font=frame_font).pack(anchor=NW)
    Checkbutton(frame, text="Two numbers with the most shows together", variable=couples, onvalue=True, offvalue=False,
                bg='#3E8E7E', activebackground="#3E8E7E", font=frame_font).pack(anchor=NW)
    Checkbutton(frame, text="Numbers appearance in lottery sequence", variable=chain_num, onvalue=True, offvalue=False,
                bg='#3E8E7E', activebackground="#3E8E7E", font=frame_font).pack(anchor=NW)
    Checkbutton(frame, text="Random built by numbers with most appearance", variable=randomByStrongNum,
                onvalue=True, offvalue=False, bg='#3E8E7E', activebackground="#3E8E7E", font=frame_font).pack(anchor=NW)
    Checkbutton(frame, text="Random numbers, add favorite numbers", activebackground="#3E8E7E",
                variable=randomNum, onvalue=True, offvalue=False, bg='#3E8E7E', font=frame_font).pack(anchor=NW)
    # TODO: place to write numbers (box)
    entry_number = Entry(frame)
    entry_number.insert(0, "Enter numbers")
    entry_number.pack(anchor=W)
    Label(frame, text="", bg='#3E8E7E').pack()                                          # For space between things

    Label(root, text="", bg='#3E8E7E').pack()                                           # For space between things
    Checkbutton(root, text="Download your ticket as text file", variable=option_download, onvalue=1,
                offvalue=0, activebackground="#3E8E7E", bg='#3E8E7E', font=small_font).pack(anchor=W)
    Label(root, text="", bg='#3E8E7E').pack()                                           # For space between things
    Button(root, text="End", command=root.quit, fg="black",
           bg='#7CD1B8', font=big_font).pack(anchor=S)                                  # End button, quit App

    root.mainloop()


def main():
    """
    Main
    :return: none
    """
    gui()
    # tests()
    # submit()
    # submit_ldb()


if __name__ == '__main__':          # Press the green button in the gutter to run the script.
    file_name = 'Lotto.csv'                                                 # The file containing lotto results
    ldb_list = []                                                           # list of the DB
    main()

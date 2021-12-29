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
global res_lst_tickt
global function_counter

file_name = 'Lotto.csv'                                                     # The file containing lotto results
ldb_list = []                                                               # list of the DB
function_counter = 0                                                        # How many functions selected


def tests():
    submit_ldb()
    # strongNumsOnlyWins()
    # couples()
    # chain_num()
    wining_dates()


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
        else:
            print(item.lotto_num)
    # print(num_list)

    # part2 - making result list
    max_strong_index = list(st_num_list).index(max(st_num_list))            # Getting strong num
    print(max_strong_index)

    result_list = np.zeros((6,), dtype=int)
    result_list_i = np.zeros((6,), dtype=int)
    for i in range(0,6):                                                    # Getting 6 number
        result_list[i] = max(num_list)
        result_list_i[i] = list(num_list).index(result_list[i])
        num_list[result_list_i[i]] = 0

    for i in range(0,6):
        num_list[result_list_i[i]] = result_list[i]

    print(num_list)
    print(result_list)
    # Result
    print(result_list_i)
    res_list = [1, 2, 3, 4, 5, 6, 7]
    return res_list


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
    result_list = np.zeros((6,), dtype=int)
    result_list_i = np.zeros((6,), dtype=int)
    for i in range(0, 6):
        result_list[i] = max(num_list)
        result_list_i[i] = list(num_list).index(result_list[i])
        num_list[result_list_i[i]] = 0

    for i in range(0, 6):
        num_list[result_list_i[i]] = result_list[i]

    print(num_list)
    print(result_list)

    print(result_list_i)                                                    # Result
    res_list = [1, 2, 3, 4, 5, 6, 7]
    return res_list


def couples():
    """
    function getting the best numbers only from wins
    :return: List the 6 number & extra (7 numbers in total)
    """
    num_list = np.zeros((38, 38), dtype=int)
    st_num_list = np.zeros((8,),dtype=int)
    for item in ldb_list:
        for a in item.six_num_arr:
            for b in item.six_num_arr:
                if a != b:
                    num_list[int(a)][int(b)] += 1
        if item.x_num < 8:
            st_num_list[item.x_num] += 1
    print(num_list)
    print(st_num_list)

    # part2 - making result list
    result_list = np.zeros((6,), dtype=int)
    result_list_i = np.zeros((6,), dtype=int)
    # for i in range(0, 6):
    #     result_list[i] = max(num_list)
    #     result_list_i[i] = list(num_list).index(result_list[i])
    #     num_list[result_list_i[i]] = 0
    #
    # for i in range(0, 6):
    #     num_list[result_list_i[i]] = result_list[i]

    print(num_list)
    print(result_list)
    print(result_list_i)
    res_list = [1, 2, 3, 4, 5, 6, 7]
    return res_list


def wining_dates():
    """
    function getting the best date to fill ticket
    :return: DO TO
    """
    wining_list = []
    # Add only wining from DB
    for item in ldb_list:
        if item.win_num > 0 or item.dbwin_num > 0:
            wining_list.append(item)

    print(len(wining_list))


def chain_num():
    """
    download csv from loto website
    :return: List the 6 number & extra (7 numbers in total)
    """
    num_list_counter = np.zeros((38,), dtype=int)   # number of shows in a row
    many_list_chain = np.zeros((38,), dtype=int)
    num_list_max = np.zeros((38,), dtype=int)
    st_num_list = np.zeros((8,), dtype=int)

    temp_six_arr = [ldb_list[0].six_num_arr[0], ldb_list[0].six_num_arr[1], ldb_list[0].six_num_arr[2],
                    ldb_list[0].six_num_arr[3], ldb_list[0].six_num_arr[4], ldb_list[0].six_num_arr[5]]
    for item in ldb_list:
        if item.lotto_num < 1841:
            break
        for temp in item.six_num_arr:
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

    # part2 - making result list
    num_list_counter = np.zeros((38,), dtype=int)
    for i in range(0, 38):
        num_list_counter[i] = num_list_max[i]*2 + many_list_chain[i]
    print(num_list_counter)

    result_list = np.zeros((6,), dtype=int)
    result_list_i = np.zeros((6,), dtype=int)

    for i in range(0, 6):
        result_list[i] = max(num_list_counter)
        result_list_i[i] = list(num_list_counter).index(result_list[i])
        num_list_counter[result_list_i[i]] = 0

    for i in range(0, 6):
        num_list_counter[result_list_i[i]] = result_list[i]

    # Result
    print(result_list_i)
    print(num_list_counter)
    # number of times the num show repeted in foing win
    print(num_list_max)

    # number of time the num were 3 time in a row
    print(many_list_chain)
    res_list = [1, 2, 3, 4, 5, 6, 7]
    return res_list

def randomBySeed():
    """
    download csv from loto website
    :return: List the 6 number & extra (7 numbers in total)
    """
    print("ddd")
    res_list = [1, 2, 3, 4, 5, 6, 7]
    return res_list


def randomByStrongNum():
    """
    download csv from loto website
    :return: List the 6 number & extra (7 numbers in total)
    """
    print("ddd")
    res_list = [1, 2, 3, 4, 5, 6, 7]
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
    h = np.random.normal(200000, 25000, 5000)
    print(graph_num)
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
    # popup("BillDa", "you have to be over 18 for buying lotto ticket")
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

    my_canvas = Canvas(top1, width=375, height=500, bg='#146356')           # Create the canvas for the ticket
    my_canvas.create_rectangle(268, 0, 272, 500, fill="black")              # Rectangle that create a black line
    x1_start = 30                                                           # Start point for oval (x1,y1,x2,y2)
    y1_start = 15
    x2_start = 60
    y2_start = 45
    btn_grph_list = []
    btn_win_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "A1", "A2", "As"]
    function_counter = 12
    for row in range(0, function_counter):
        my_canvas.create_text(x1_start - 15, y1_start + 15 + (row * 40), fill="black", font=font, text=row + 1)
        for col in range(0, 6):
            my_canvas.create_oval(x1_start + (col * 40), y1_start + (row * 40), x2_start + (col * 40), y2_start + (row * 40), fill="#F90716")
            my_canvas.create_text(x1_start + 15 + (col * 40), y1_start + 15, fill="black", font=font, text="33")
        # Strong number
        my_canvas.create_oval(250 + x1_start, y1_start + (row * 40), 250 + x2_start, y2_start + (row * 40), fill="red")
        my_canvas.create_text(265 + x1_start, y1_start + 15 + (row * 40), fill="black", font=font, text="6")
        # Graph button
        btn_grph_list.append(Button(my_canvas, text=btn_win_list[row], command=lambda: graphs(row)))
        btn_grph_list[row].configure(width=5, activebackground="green", relief=FLAT)
        # # btn_win_list.append(my_canvas.create_window(320, y1_start + (row * 40), anchor=NW, window=btn_grph_list[row]))
        # my_canvas.create_window(320, y1_start + (row * 40), anchor=NW, window=btn_grph_list[row])
    coun = 0
    for btn in btn_grph_list:
        my_canvas.create_window(320, y1_start + (coun * 40), anchor=NW, window=btn)
        coun += 1
    # button1 = Button(my_canvas, text="A", command=lambda: graphs(0), anchor=W)
    # button1.configure(width=5, activebackground="#33B5E5", relief=FLAT)
    #
    #
    # button2 = Button(my_canvas, text="B", command=lambda: graphs(1), anchor=W)
    # button2.configure(width=5, activebackground="#33B5E5", relief=FLAT)
    #
    # my_canvas.create_window(320, 15, anchor=NW, window=button1)
    # my_canvas.create_window(320, 55, anchor=NW, window=button2)

    my_canvas.pack(padx=5, pady=5)
    Button(top1, text="End", command=root.quit, fg="black", bg='#7CD1B8').pack()



def gui():
    """
    Main window (GUI), start menu
    :return: none
    """
    global root
    global option_download
    global strongNums
    global strongNumsOnlyWins
    global couples
    global chain_num
    result_list = []

    root = Tk()                                                             # Configure main window
    root.minsize(400, 400)
    root.title("Lotto App")
    root.config(bg='#3E8E7E')

    # Configure start menu
    strongNums = IntVar()
    strongNumsOnlyWins = IntVar()
    couples = IntVar()
    chain_num = IntVar()
    option_download = IntVar()

    Button(root, text="Start", command=start_button,
           fg='#041C32', bg='#7CD1B8').pack(anchor=N)                                   # Start button, create ticket

    Checkbutton(root, text="option download", variable=option_download, onvalue=1, offvalue=0,
                activebackground="#3E8E7E", bg='#3E8E7E', fg='black').pack()

    frame = LabelFrame(root, text="Functions", padx=10, pady=30, bg='#3E8E7E')
    frame.pack(padx=10, pady=10)

    Checkbutton(frame, text="strongNums", variable=strongNums, onvalue=1, offvalue=0,
                bg='#3E8E7E', fg='black').pack(anchor=NW)
    Checkbutton(frame, text="strongNumsOnlyWins", variable=strongNumsOnlyWins, onvalue=1, offvalue=0,
                bg='#3E8E7E', fg='black').pack(anchor=NW)
    Checkbutton(frame, text="couples", variable=couples, onvalue=1, offvalue=0,
                bg='#3E8E7E', fg='black').pack(anchor=NW)
    Checkbutton(frame, text="chain_num", variable=chain_num, onvalue=1, offvalue=0,
                bg='#3E8E7E', fg='black').pack(anchor=NW)

    Button(root, text="End", command=root.quit, fg="black", bg='#7CD1B8').pack(anchor=S)    # End button, quit App

    root.mainloop()


def main():
    """
    Main
    :return: none
    """
    print("main")
    # gui()
    tests()
# submit()
# submit_ldb()


if __name__ == '__main__':          # Press the green button in the gutter to run the script.
    main()

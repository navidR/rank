#!/bin/python3
from gi.repository import Gtk, GObject
import socket, time, random, sys

# Variable
MAX_BUF = 100
TIMER_INTERVAL = 1000
UPDATER_INTERVAL = 5000
TIME_FORMAT = '%X'
TEAM_NUMBER = 15
#FINISHED = False

# String For Glade
BUILDER_FILE_STR = "shower.glade"
TREEVIEW_STR = "treeview"
WINDOW_STR = "window"
LABEL_STR = "label"

if len(sys.argv) < 4:
    print("You should provide server IP addr, Remaing Hour, Remaining Minute")
    sys.exit()
HOUR = int(sys.argv[2])
MINUTE = int(sys.argv[3])
ADDRESS = (sys.argv[1], 8880)
TEAM_NAME = "team-name.txt"
TEAM_RESULT = "team-result.txt"

# Events
DELETE_EVENT = "delete-event"
SHOW_EVENT = "show"

class Update_Interval():
    def __init__(self, hour, minute):
        self.hour = 5
        self.minute = 0
        self.second = 0
        self.finished = False
    def __call__(self):
        print("__call__ updater")
        if self.finished == True:
            print("contest finished")
            return True
        if self.second == 0:
            if self.minute == 0:
                if self.hour == 0:
                    self.finished = True
                else:
                    self.hour -= 1
                    self.minute = 59
                    self.second = 59
            else:
                self.minute -= 1
        else:
            self.second -= 1
            timer.set_text(time.strftime(TIME_FORMAT) + ", Remaining : " + str(self.hour) + ":" + str(self.minute) + ":" + str(self.second))
        return True

class Update_Table():
    def __init__(self, treeview):
        # number, name, point, penalty, Used Time, a, b, c, d, e, f, h
        #                               0 ,  1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 , 10 , 11 , 12
        self.liststore = Gtk.ListStore(int, str, int, int, int, str, str, str, str, str, str, str, str)
        for i in range(1, TEAM_NUMBER + 1):
            self.liststore.append(list((i, 'unknown', 0, 0, 0, '✗', '✗', '✗', '✗', '✗', '✗', '✗', '✗')))

        #self.liststore = Gtk.ListStore(int, str)
        #for i in range(0, 24):
        #    self.liststore.append(list((i, '1')))


        self.treeview = treeview
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='#',  cell_renderer=renderer, text=0)
        column.set_sort_column_id(0)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='Name', cell_renderer=renderer, text=1)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='Point', cell_renderer=renderer, text=2)
        column.set_sort_column_id(2)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='Penalty', cell_renderer=renderer, text=3)
        column.set_sort_column_id(3)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='Last Time Checkpoint', cell_renderer=renderer, text=4)
        column.set_sort_column_id(4)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='A', cell_renderer=renderer, text=5)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='B', cell_renderer=renderer, text=6)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='C', cell_renderer=renderer, text=7)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='D', cell_renderer=renderer, text=8)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='E', cell_renderer=renderer, text=9)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='F', cell_renderer=renderer, text=10)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='G', cell_renderer=renderer, text=11)
        self.treeview.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(title='H', cell_renderer=renderer, text=12)
        
        self.treeview.append_column(column)
        self.treeview.set_model(self.liststore)


        # Need to Remove
        #for i in range(0, TEAM_NUMBER):
        #    self.liststore[i][2] = random.randint(1,80)
        #    self.liststore[i][3] = random.randint(1,80)
        #    self.liststore[i][4] = random.randint(1,80)
        # Just for Testing Case

    def __call__(self, finished):
        print("update_table")
        # Open Socket to Server and Read from Socket
        team_name_str = ""
        team_result_str = ""
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if finished == True:
            return True
        try:
            self.s.connect(ADDRESS)
        except ConnectionRefusedError:
            print("ConnectionRefusedError Exception, Please Connect to Server")
            return True
        while True:
            t = bytes.decode(self.s.recv(MAX_BUF))
            if len(t) != 0:
                team_name_str += t
            else:
                break
        #print(time.strftime(TIME_FORMAT) + " => " + str(team_name_str))
        self.s.close()
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.s.connect(ADDRESS)
        except ConnectionRefusedError:
            print("ConnectionRefusedError Exception, Please Connect to Server")
            return True
        while True:
            t = bytes.decode(self.s.recv(MAX_BUF))
            if len(t) != 0:
                team_result_str += t
            else:
                break
        #print(time.strftime(TIME_FORMAT) + " => " + str(team_result_str))
        self.s.close()
        team_name = open(TEAM_NAME, 'w')
        team_name.write(team_name_str)
        team_name.close()
        team_result = open(TEAM_RESULT, 'w')
        team_result.write(team_result_str)
        team_result.close()
        team_name_str.strip()
        l = team_name_str.split('\n')
        for i in range(0, len(l) - 1):
            self.liststore[i][1] = l[i]

        team_result_str.strip()
        l = team_result_str.split('\n')
        #print(l)
        for i in range(0, TEAM_NUMBER):
            plist = list()
            p = 0 # Penalty
            s = 0 # Solved
            m = 0 # Max Time
            #print("i :" + str(i) )
            for j in range(0, len(l) - 1):
                team_num, question, r = l[j].split(':')
                #print("team_num : " + team_num)
                #print("question: " + question)
                #print("r : " + r)
                if int(team_num) == i: # This is our team
                    if r == '-':
                        plist.append(int(question))
                    else:
                        s += 1
                        self.liststore[i - 1][5 + int(question)] = '✔' # Solved Index
                        if m < int(r):
                            m = int(r)
                        if int(question) in plist:
                            p += 1
            self.liststore[i - 1][2] = s * 10 # Solved Index
            self.liststore[i - 1][3] = p # Penalty Index
            self.liststore[i - 1][4] = m # Max Time Index
        
        return True

# Create Gtk Builder
builder = Gtk.Builder()
builder.add_from_file(BUILDER_FILE_STR)

# Loading Window
window = builder.get_object(WINDOW_STR)
window.connect(DELETE_EVENT, Gtk.main_quit)
window.set_title("University of Mohaghegh Ardebili, ACM Contest")
#window.maximize()
#window.set_decorated(False)

# Loading TreeView
treeview = builder.get_object(TREEVIEW_STR)

# Timer Label
timer = builder.get_object(LABEL_STR)

timer_updater = Update_Interval(HOUR, MINUTE)
table_updater = Update_Table(treeview)
GObject.timeout_add(TIMER_INTERVAL, timer_updater)
GObject.timeout_add(UPDATER_INTERVAL, table_updater, timer_updater.finished)

window.show_all()
Gtk.main()

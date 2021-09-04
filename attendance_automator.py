import re
import os
import datetime
import subprocess as sp

# -\d+-\w+(?: \w+)* matches the -00-Name Surname
# -(\d+)- matches rollnumber
# (\w+(?: \w+)*) matches the name


class open_file:

    # Takes file_location input and checks if file exists
    def __init__(self, file_location):
        self.file_location = file_location
        if (os.path.isfile(file_location)):
            file_data = open(file_location, "r")
            content = file_data.read()
            file_data.close
        else:
            print("[ FILE DO NOT EXIST ]")
        self.process(content)

    def process(self, content):
        # Regular Expression extracts important data from the input file
        pattern = r"[SYCS|Sycs|sycs|FYCS|TYCS|Tycs|Fycs]+-\d+-\w+(?: \w+)*"
        # Add more prefixes in the above line to get more Classes recognized
        processed_data = re.findall(pattern, content)
        print("[Removing Duplicates...]")
        self.remove_duplicates(processed_data)

    # Removing duplicate entrys from saved chat
    def remove_duplicates(self, data):
        self.temp_lst = []
        for i in data:
            if i not in self.temp_lst:
                self.temp_lst.append(i)
        print("[PRESENT STUDENTS]")
        self.temp_lst.sort()
        for i in self.temp_lst:
            print(i)
        self.roll_no(self.temp_lst)

    def roll_no(self, temp_list):
        d_process = str(temp_list)
        # -(\d+)-(\w+(?: \w+)*)
        pat = r"-(\d+)-"
        self.roll_no = re.findall(pat, d_process)
        self.roll_no.sort()
        temp_arr = []
        for i in self.roll_no:
            if i not in temp_arr:
                temp_arr.append(i)
        self.roll_no = temp_arr

    def data_for_saving(self):
        return self.temp_lst, self.roll_no


class save_file:

    def __init__(self, data, location, meeting_date, class_name, total_studs):
        self.data = data
        self.location = location
        self.meeting_date = meeting_date
        self.class_name = class_name
        self.total_studs = total_studs
        self.format_roll()

    def format_roll(self):
        roll_no_ = self.data[1]
        sorted_roll_no_ = []
        for i in range(0, len(roll_no_)):
            roll_no_[i] = int(roll_no_[i])
        roll_no_.sort()
        print("[Preset Students] = ", roll_no_)
        self._roll_no_print = roll_no_
        self.check_absent(roll_no_)

    def check_absent(self, roll_no):
        try:
            total_students = int(self.total_studs)
        except ValueError:
            total_students = 46
            print("[INTEGER WAS EXPECTED FOR TOTAL STUDENTS]")
            print("[USING DEFAULT VALUE FOR TOTAL STUDENTS AS 45]")
        self.absent_studs = []
        for i in range(1, total_students):
            if i not in roll_no:
                self.absent_studs.append(i)
        print("[Absent Students] = ", self.absent_studs)
        self.save_data()

    def save_data(self):
        _students_print = self.data[0]
        time_ = datetime.datetime.now()
        year = time_.strftime("%d %B, %Y")
        time_now = time_.strftime("%I:%M %p")
        file_save = open(self.location, "a+")
        file_save.write(
            "DATA PROCESSED ON : [ {} ] [ {} ]".format(year, time_now))
        file_save.write("\n")
        file_save.write("\n")
        file_save.write("MEETING OCCURRED ON : {} ".format(self.meeting_date))
        file_save.write("\n")
        file_save.write("\n")
        file_save.write("CLASS NAME : {} ".format(self.class_name))
        file_save.write("\n")
        file_save.write("\n")
        file_save.write('[PRESENT STUDENTS]')
        file_save.write("\n")
        for i in _students_print:
            file_save.write(i)
            file_save.write("\n")
        file_save.write("\n")
        file_save.write("[Present Students] = {} ".format(self._roll_no_print))
        file_save.write("\n")
        file_save.write("[Absent Students] = {} ".format(self.absent_studs))
        file_save.write("\n")
        file_save.write("\n")
        file_save.write("Total Absent :{} ".format(len(self.absent_studs)))
        file_save.write("\n")
        file_save.write("\n")
        file_save.write("Total Present :{} ".format(len(self._roll_no_print)))
        file_save.write("\n")
        file_save.write("\n")
        file_save.write("\n")
        file_save.write(
            "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        file_save.write("\n")
        file_save.close()


print(" ---<< [ Automate Zoom Attendance ] >>--- ")
print()
file_location = input("ENTER ABSOLUTE FILE LOCATION :>>> ")
date_of_meeting = input("ENTER DATE OF MEETING :>> ")
class_name = input("ENTER CLASS NAME :>> ")
try:
    total_students_in_class = int(input("TOTAL STUDENTS IN CLASS :>> "))
    total_students_in_class += 1
except ValueError:
    print("ENTER INTEGERS ONLY")
    print("45 STUDENTS BY DEFAULT SELECTED")
    total_students_in_class = 46
except TypeError:
    total_students_in_class = 46
x = input("DO YOU WANT TO OPEN THE FILE AFTER PROCESSING ? (Y OR N) :>> ")
# file_location = "S:/Python/Project_Z/zoom_test_data.txt"
try:
    file1 = open_file(file_location)
    data_f = file1.data_for_saving()
    save_file(data_f, "attendance_file.txt", date_of_meeting,
              class_name, total_students_in_class)
except:
    print("[ INVALID FILE ]")


program_name = "notepad.exe"
output_file_name = "attendance_file.txt"
if x.upper() == 'Y':
    sp.Popen([program_name, output_file_name])

k = input('Press Enter to Close....')

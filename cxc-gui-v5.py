import shutil
from os.path import join, isfile, isdir, exists
from os import listdir, makedirs
import numpy as np
import pandas as pd 
import re
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

'''
********* FUNCTIONS **************
'''
def setUpTeamsDirs(report_num,teams_list,destination_dir,mentor):
    # create a report folder
    report_dir = join(destination_dir,mentor,"Report "+str(report_num))
    if not exists(report_dir):
        makedirs(report_dir)
    
    # create team folders in report folder
    for team in teams_list:
        team_dir = join(destination_dir,mentor,report_dir,team)
        if not exists(team_dir):
            makedirs(team_dir)
    return 

def organizeFiles():
    lbl_terminal.configure(state='normal')
    lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "   Organizing...\n")
    if not exists(input_mentorslistfile.get()) or not exists(input_studentslistfile.get()):
        lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "One or both files are invalid. Check that both files exist.\n")
        return
    if not exists(input_sourcepath.get()) or not exists(input_destpath.get()):
        lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "One or both paths are invalid. Check that both paths exist.\n")
        return
    if report_num == "Set Report Number":
        lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "Set report number before sorting!\n")
        return

    mentor_team_list = pd.read_csv(input_mentorslistfile.get())
    students_team_list = pd.read_csv(input_studentslistfile.get())
    submission_dir = input_sourcepath.get()
    destination_dir = input_destpath.get()
    report_num = set_reportnum()
    # student_team_list = pd.read_csv('/Users/mercedesgonzalez/Dropbox (GaTech)/CREATE_X/gui/student-team-list.csv')

    # create list of unique mentors
    mentor_list = mentor_team_list.Mentor.unique()
    print(mentor_list)

    for mentor in mentor_list:
        # create mentor folders with their names
        mentor_dir = join(destination_dir,mentor)
        if not exists(mentor_dir):
            makedirs(mentor_dir)
            lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "   Created directory for " + mentor + "\n")

        # create reports folders and the teams folders inside
        teams_list = mentor_team_list[mentor_team_list["Mentor"] == mentor]["Team"].tolist()
        setUpTeamsDirs(1,teams_list,destination_dir,mentor)
        setUpTeamsDirs(2,teams_list,destination_dir,mentor)
        setUpTeamsDirs(3,teams_list,destination_dir,mentor)

    # ____________ at this point all folders are created. _______________

    # based on team files submitted, sort the files into their respective folders.
    team_submissions_list = listdir(submission_dir) # list of filenames submitted
    for fn in team_submissions_list:
        # copy the team submissions 
        if fn.startswith("team"):
            team_name = re.split("_", fn)[0]
            team_num = re.sub("team","",team_name)
            mentor_dir = mentor_team_list[mentor_team_list["Team"] == "Team "+team_num]["Mentor"].to_string(index=False)
            src_path = join(submission_dir,fn)
            dst_path = join(destination_dir,mentor_dir,"Report "+str(report_num),"Team "+team_num,fn)
            print("source: ",src_path)
            print("destin: ",dst_path)
            shutil.copy(src_path, dst_path)
            lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "   sorted: team " + str(team_num) + "\n")
        else:
            name_str = re.split("_",fn)[0]
            if name_str in students_team_list.values:
                mentor_dir = students_team_list[students_team_list["Name"] == name_str]["Mentor"].to_string(index=False)
                team_dir = students_team_list[students_team_list["Name"] == name_str]["Team"].to_string(index=False)
                src_path = join(submission_dir,fn)
                dst_path = join(destination_dir,mentor_dir,"Report "+str(report_num),team_dir,fn)
                print("source: ",src_path)
                print("destin: ",dst_path)
                shutil.copy(src_path, dst_path)
                lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "   sorted: " + name_str + "\n")
            else: 
                lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "   NOT SORTED: " + name_str + "\n")
                src_path = join(submission_dir,fn)
                dst_path = join(destination_dir,"not-found-files")
                if not exists(dst_path):
                    makedirs(dst_path)
                dst_path = join(dst_path,fn)
                print("source: ",src_path)
                print("destin: ",dst_path)
                shutil.copy(src_path, dst_path)
    lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + '   Files are sorted!\n')
    lbl_terminal.configure(state='disabled')

    return

def browse_source():
    input_sourcepath.delete(0,'end')
    input_sourcepath.insert(0,filedialog.askdirectory())

def browse_dest():
    input_destpath.delete(0,'end')
    input_destpath.insert(0,filedialog.askdirectory())

def browse_mentors():
    input_mentorslistfile.delete(0,'end')
    input_mentorslistfile.insert(0,filedialog.askopenfilename())

def browse_students():
    input_studentslistfile.delete(0,'end')
    input_studentslistfile.insert(0,filedialog.askopenfilename())

def set_reportnum():
    return report_num.get()

'''
******* GUI *********
'''

# Set up the window
window = tk.Tk()
window.title("Create-X Capstone: File Sorter")
window.resizable(width=False, height=False)
window.geometry("700x600+200+200")

main_frame = tk.Frame(master=window)
default_color = main_frame.cget("bg")
terminal_frame = tk.Frame(master=window, height=200)

#ADDING A SCROLLBAR
scroll = tk.Scrollbar(terminal_frame, orient="vertical")
scroll.grid(row=0, column=1, sticky='ns')

report_num = tk.StringVar()
input_sourcepath = tk.Entry(master=main_frame, width=50)
input_destpath = tk.Entry(master=main_frame, width=50)
input_mentorslistfile = tk.Entry(master=main_frame, width=50)
input_reportnum_optionmenu = tk.OptionMenu(main_frame,report_num,"1","2","3")
input_studentslistfile = tk.Entry(master=main_frame, width = 50)
# input_sourcepath.insert(0,"/Users/mercedesgonzalez/Downloads/finalpresent/")
# input_destpath.insert(0,"/Users/mercedesgonzalez/Dropbox (GaTech)/CREATE_X/Create-X Capstone Spring 2023 Grading")
# input_mentorslistfile.insert(0,"/Users/mercedesgonzalez/Dropbox (GaTech)/CREATE_X/gui/mentor-team-list-sp2023.csv")
# input_studentslistfile.insert(0,"/Users/mercedesgonzalez/Dropbox (GaTech)/CREATE_X/gui/student-team-list-sp2023.csv")
report_num.set("Set Report Number")

# Labels
lbl_sourcepath = tk.Label(master=main_frame, text="Source Path")
lbl_destpath = tk.Label(master=main_frame, text="Destination Path")
lbl_mentorslist = tk.Label(master=main_frame, text="Mentors List (.csv)")
lbl_studentslist = tk.Label(master=main_frame, text="Students List (.csv)")
lbl_reportnum = tk.Label(master=main_frame, text="Report #")
lbl_terminal = tk.Text(master=terminal_frame,yscrollcommand=scroll.set,bg=default_color,relief=tk.RAISED)

# Create the conversion Button and result display Label
btn_sort = tk.Button(master=main_frame, text="SORT", command=organizeFiles)
btn_browsesource = tk.Button(master=main_frame, text="Browse", command=browse_source)
btn_browsedest = tk.Button(master=main_frame, text="Browse", command=browse_dest)
btn_browsementors = tk.Button(master=main_frame, text="Browse", command=browse_mentors)
btn_browsestudents = tk.Button(master=main_frame, text="Browse", command=browse_students)

# Set up the layout using the .grid() geometry manager
input_sourcepath.grid(row=0, column=1, sticky="e")
input_destpath.grid(row=1, column=1, sticky="e")
input_mentorslistfile.grid(row=2, column=1, sticky="e")
input_studentslistfile.grid(row=3, column=1,sticky="e")
input_reportnum_optionmenu.grid(row=4, column=1,sticky="w")

lbl_sourcepath.grid(row=0, column=0, sticky="w")
lbl_destpath.grid(row=1, column=0, sticky="w")
lbl_mentorslist.grid(row=2, column=0, sticky="w")
lbl_studentslist.grid(row=3, column=0, sticky="w")
lbl_reportnum.grid(row=4, column=0, sticky="w")
lbl_terminal.grid(row=0, column=0, sticky="e",padx=10, pady=10)

main_frame.grid(row=0, column=0, padx=10)
terminal_frame.grid(row=1, column=0, padx=10)

btn_sort.grid(row=4, column=2, pady=10, padx=10)
btn_browsesource.grid(row=0, column=2, pady=10)
btn_browsedest.grid(row=1, column=2, pady=10)
btn_browsementors.grid(row=2, column=2, pady=10)
btn_browsestudents.grid(row=3, column=2, pady=10)

scroll.config(command=lbl_terminal.yview)


lbl_terminal.insert(tk.END, str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")) + "   Ready to sort.\n\n")
lbl_terminal.configure(state='disabled')

# Run the application
window.mainloop()
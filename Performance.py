from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont

import os
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time

def OnMouseWheel(event):
    my_canvas.yview_scroll(-1*(event.delta // 120), "units")

def check_password():
    global password
    password = ""
    password = password_entry.get()

    if password == "":
        password_entry.delete(0, END)
        messagebox.showinfo("", "Blank not allowed")
    elif password == "0000":
        password_entry.delete(0, END)
        messagebox.showinfo("", "Login Success")
        start_window.destroy()
        general()
    else:
        password_entry.delete(0, END)
        messagebox.showinfo("", "Incorrect password")
    return

#-----------------------------------------------------------------------------------------------------------------------

def work():
    work_period = True
    global work_window

    #moves to top of canvas
    my_canvas.yview_moveto('0.0')

    #Create frame within canvas
    work_window = Frame(my_canvas, bg='#121212', width=w, height=h, relief=FLAT)


    # Add new frame to window in canvas
    my_canvas.create_window((0, 0), window=work_window, anchor="nw")
    #work_window.place(x=0, y=0)


    # Work entries
    global hours_worked_entry
    global valuable_learning_entry
    global work_projects_entry

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    work_window_label = Label(work_window, text="Work Window.", bg='#121212', fg='white', font=('Times New Roman bold', 30), justify="center").grid(row=0, column=0, columnspan=4, padx=0, pady=10)

    # Creating General Table and if it exists connects cursor
    c.execute("""CREATE TABLE IF NOT EXISTS
           Work(
               Date TEXT PRIMARY KEY,
               Hours_worked FLOAT,
               Valuable_learning TEXT,
               Work_projects TEXT,
               Total_work FLOAT,
               Overall_work FLOAT
           )
       """)

    #ask work questions
    hours_worked_label = Label(work_window, text="How many hours have you worked, PRODUCTIVELY, this week?: ", bg='#121212',
                                 fg='white', font=('Times New Roman bold', 15)).grid(row=1, column=0, padx=20, pady=20)
    learning_label = Label(work_window, text="Have you learnt anything valuable from work this week?: ", bg='#121212', fg='white',
                             font=('Times New Roman bold', 15)).grid(row=2, column=0, padx=20, pady=20)
    work_projects_label = Label(work_window, text="Have you completed or progressed through any work projects you are currently assigned to?\n(Tick \"NONE\" if you do not have any projects): ",
                               bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=3, column=0, padx=20, pady=20)

    hours_worked_entry = Entry(work_window, width=20, font=('Times New Roman bold', 15))
    hours_worked_entry.grid(row=1, column=1, ipady=15, padx=20, pady=20)

    valuable_learning_entry = IntVar()
    valuable_learning_entry.set('None')
    global valuable_learning_button_1
    global valuable_learning_button_2
    valuable_learning_button_1 = Radiobutton(work_window, text="Yes", variable=valuable_learning_entry, value=1)
    valuable_learning_button_1.grid(row=2, column=1)
    valuable_learning_button_2 = Radiobutton(work_window, text="No", variable=valuable_learning_entry, value=0)
    valuable_learning_button_2.grid(row=2, column=2)

    work_projects_entry = IntVar()
    work_projects_entry.set('None')
    global work_projects_button_1
    global work_projects_button_2
    global work_projects_button_3
    work_projects_button_1 = Radiobutton(work_window, text="Yes", variable=work_projects_entry, value=values[2])
    work_projects_button_1.grid(row=3, column=1)
    work_projects_button_2 = Radiobutton(work_window, text="No", variable=work_projects_entry, value=values[0])
    work_projects_button_2.grid(row=3, column=2)
    work_projects_button_3 = Radiobutton(work_window, text="None", variable=work_projects_entry, value=values[1])
    work_projects_button_3.grid(row=3, column=3, padx=50)

    global view_work_btn
    global submit_work_btn
    submit_work_btn = Button(work_window, text="Submit", bg='#121212', fg='white', font=('Arial bold', 15),
                                command=submit_work_info, width=30)
    submit_work_btn.grid(row=4, column=0, columnspan=3, pady=20)
    view_work_btn = Button(work_window, text="View Data", bg='#121212', fg='white', font=('Arial bold', 15),
                              command=view_work_info, width=30)
    view_work_btn.grid(row=5, column=0, columnspan=3, pady=20)
    view_work_btn['state'] = DISABLED

    global close_work_btn
    close_work_btn = Button(work_window, text="Close Table", relief=RAISED, font=('Arial bold', 15),
                           command=close_work_table, width=20)
    close_work_btn.grid(row=7, column=0, columnspan=2, pady=20, padx=(150, 0))
    close_work_btn['state'] = DISABLED

    global view_wrk_performance
    view_wrk_performance = Button(work_window, text="View Peformance", bg='#121212', fg='white', font=('Arial bold', 15), command=view_work_performance, width=30)
    view_wrk_performance['state'] = DISABLED
    view_wrk_performance.grid(row=8, column=0, columnspan=3, pady=20)

    global open_overall_work_btn
    open_overall_work_btn = Button(work_window, text="View Result", bg='#121212', fg='white',
                                  font=('Arial bold', 15), command=overall_work_page, width=30)
    open_overall_work_btn['state'] = DISABLED
    open_overall_work_btn.grid(row=9, column=0, columnspan=3, pady=20)

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()

    return

def submit_work_info():
    global hours_worked
    global valuable_learning
    global work_projects

    # Work radio database entries
    global valuable_learning_database_entry
    global work_projects_database_entry

    try:
        hours_worked = float(hours_worked_entry.get())
    except ValueError:
        hours_worked_entry.config(bg="Red")
        messagebox.showinfo("", "You entered a string in the box highlighted in red. Please enter a number.")
        hours_worked_entry.delete(0, END)

    hours_worked = float(hours_worked_entry.get())

    while (hours_worked > 140) or (hours_worked < 0):
        hours_worked_entry.config(bg="Red")
        messagebox.showinfo("", "You cannot exceed 140 or subceed 0 work hours in a week. Re-enter a POSITIVE value equal to, or less than 140 in the box highlighted in red.")
        hours_worked_entry.delete(0, END)
        hours_worked = float(hours_worked_entry.get())
    hours_worked_entry.config(bg="White")

#-----------------------------------------------------------------------------------------------------------------------

    try:
        valuable_learning = valuable_learning_entry.get()
    except TclError:
        valuable_learning_button_1.config(bg="Red")
        valuable_learning_button_2.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if valuable_learning == 1:
        valuable_learning_database_entry = "Yes"
    else:
        valuable_learning_database_entry = "No"

#-----------------------------------------------------------------------------------------------------------------------

    try:
        work_projects = work_projects_entry.get()
    except TclError:
        work_projects_button_1.config(bg="Red")
        work_projects_button_2.config(bg="Red")
        work_projects_button_3.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if work_projects == 1:
        work_projects_database_entry = "Yes"
    elif work_projects == -1:
        work_projects_database_entry = "No"
    else:
        work_projects_database_entry = "None"

#-----------------------------------------------------------------------------------------------------------------------

    global total_work
    global overall_work
    total_work = float(hours_worked) + float(valuable_learning) + float(work_projects)
    x = (float(total_general) + float(total_work)) / 10
    overall_work = float("{:.2f}".format(x))

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # Add values to database
    # Insert into table
    c.execute(
        "INSERT INTO Work VALUES(:date, :hours_worked, :valuable_learning, :work_projects, :total_work, :overall_work)",
        {
            'date': current_time,
            'hours_worked': hours_worked,
            'valuable_learning': valuable_learning_database_entry,
            'work_projects': work_projects_database_entry,
            'total_work': total_work,
            'overall_work': overall_work
        })

    valuable_learning_button_1.config(bg="White")
    valuable_learning_button_2.config(bg="White")
    work_projects_button_1.config(bg="White")
    work_projects_button_2.config(bg="White")
    work_projects_button_3.config(bg="White")

    messagebox.showinfo("", "Your data has been submitted.")

    # Clear Boxes
    # clear the text boxes
    hours_worked_entry.delete(0, END)
    valuable_learning_entry.set('None')
    work_projects_entry.set('None')

    view_wrk_performance['state'] = NORMAL
    view_work_btn['state'] = NORMAL
    submit_work_btn['state'] = DISABLED

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()

    return

def view_work_info():
    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # Present table
    # Query the database
    c.execute("SELECT *, oid FROM Work")
    records = c.fetchall()

    # Add style for treeview
    style = ttk.Style()
    style.theme_use('default')

    # configure treeview colours
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="Black",
                    rowheight=30,
                    fieldbackground="#D3D3D3")

    # Change selected colour
    style.map('Treeview',
              background=[('selected', "#347083")]
              )

    # Create a Treeview frame
    global tree_frame_work
    tree_frame_work = Frame(work_window)
    tree_frame_work.grid(row=6, column=0, columnspan=10, pady=50)

    # Create a Treeview scrollbar
    tree_scroll_work = Scrollbar(tree_frame_work)
    tree_scroll_work.grid(row=0, column=1, sticky=NS)

    # Create treeview
    work_tree = ttk.Treeview(tree_frame_work, yscrollcommand=tree_scroll_work.set, selectmode="extended")
    work_tree.grid(row=0, column=0)

    # Configure scrollbar
    tree_scroll_work.config(command=work_tree.yview)

    # Define columns
    work_tree['columns'] = ("Date", "Hours Worked", "Valuable Learning", "Work Projects", "Total Work Score", "Overall Work Score", "Week No.")

    # Format columns
    work_tree.column("#0", width=0, stretch=NO)
    work_tree.column("Date", anchor=W, width=140)
    work_tree.column("Hours Worked", anchor=CENTER, width=100)
    work_tree.column("Valuable Learning", anchor=CENTER, width=100)
    work_tree.column("Work Projects", anchor=CENTER, width=100)
    work_tree.column("Total Work Score", anchor=CENTER, width=140)
    work_tree.column("Overall Work Score", anchor=CENTER, width=140)
    work_tree.column("Week No.", anchor=CENTER, width=100)

    # Create headings
    work_tree.heading("#0", text="", anchor=CENTER)
    work_tree.heading("Date", text="Date", anchor=CENTER)
    work_tree.heading("Hours Worked", text="Hours Worked", anchor=CENTER)
    work_tree.heading("Valuable Learning", text="Valuable Learning", anchor=CENTER)
    work_tree.heading("Work Projects", text="Projects", anchor=CENTER)
    work_tree.heading("Total Work Score", text="Total Work Score", anchor=CENTER)
    work_tree.heading("Overall Work Score", text="Overall Work Score", anchor=CENTER)
    work_tree.heading("Week No.", text="Week No.", anchor=CENTER)

    # Create Stripped Row tags
    work_tree.tag_configure('oddrow', background="white")
    work_tree.tag_configure('evenrow', background="light blue")

    # Add data to screen
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            work_tree.insert(parent='', index='end', iid=count, text='', value=(
            record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
        else:
            work_tree.insert(parent='', index='end', iid=count, text='', value=(
            record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',))
        # increment counter
        count += 1

    close_work_btn['state'] = NORMAL
    view_work_btn['state'] = DISABLED

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

def close_work_table():
    tree_frame_work.destroy()
    close_work_btn['state'] = DISABLED
    view_work_btn['state'] = NORMAL

def view_work_performance():
    view_wrk_performance.destroy()
    if total_work == 42:
        work_performance = Label(work_window, text="Average", bg='#D53600', fg='Black', font=('Arial bold', 15),
                                relief=SUNKEN).grid(row=8, column=0, padx=0, pady=20)
    elif total_work < 42:
        work_performance = Label(work_window, text="Unsatisfactory", bg='Dark Red', fg='Black',
                                font=('Arial bold', 15), relief=SUNKEN).grid(row=8, column=0, padx=0, pady=20)
    elif total_work > 42:
        work_performance = Label(work_window, text="Magnificent", bg='Dark Green', fg='Black',
                                font=('Arial bold', 15), relief=SUNKEN).grid(row=8, column=0, padx=0, pady=20)

    open_overall_work_btn['state'] = NORMAL
    return

def work_comments():
    work_comments = []
    global work_comments_text
    work_comments_text = ""
    if float(hours_worked) < 40:
        work_comments.append("You have to work more hours to get more income for investing.\n")
    if valuable_learning < 1:
        work_comments.append("Try your best to learn something new(that is valuable) this week.\n")
    if work_projects == 0:
        work_comments.append("Look for your own personal project to do OR sharpen the skills you already have.\n")
    elif work_projects == -1:
        work_comments.append("Hurry up and finish that project.\n")
    if overall_work == 6.85:
        work_comments.append("You are on average. Do better next week.\n")

    for i in range(0, len(work_comments)):
        work_comments_text = work_comments_text + work_comments[i]
        i += 1
    return

def overall_work_page():
    work_window.destroy()
    general_comments()
    work_comments()
    global overall_work_window

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # get values from database
    c.execute('SELECT Overall_work FROM Work')
    overall_work_list = []

    data = c.fetchall()

    for row in data:
        overall_work_list.append(row[0])

    index = len(overall_work_list) - 1
    reference = index - 1

    # moves to top of canvas
    my_canvas.yview_moveto('0.0')

    # Create frame within canvas
    overall_work_window = Frame(my_canvas, bg='#121212', width=w, height=h, relief=FLAT)

    # Add new frame to window in canvas
    my_canvas.create_window((0, 0), window=overall_work_window, anchor="nw")

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=overall_work_list[index],
        title={'text': "Overall Work Performance", 'font': {'size': 20}},
        delta={'reference': overall_work_list[reference]},
        gauge={
            'axis': {'range': [None, 18], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 3.425], 'color': 'red'},
                {'range': [3.425, 6.85], 'color': '#D53600'},
                {'range': [6.85, 9.925], 'color': 'lightgreen'},
                {'range': [9.925, 13], 'color': 'forestgreen'},
                {'range': [13, 18], 'color': 'darkgreen'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 16.2}}))

    fig.write_html('Work performance.html', auto_open=True)

    if gen_comments_text == "":
        comments_label = Label(overall_work_window, text="General Comments:\n\nNo comments", bg='#121212', fg='green', font=('Times new roman', 30), justify=CENTER).grid(row=0, column=0, columnspan=2, pady=20)
    else:
        comments_label = Label(overall_work_window, text="General Comments:\n\n%s"%(gen_comments_text), bg='#121212', fg='red', font=('Times new roman', 30), justify=CENTER).grid(row=0, column=0, columnspan=2, pady=20)

    if work_comments_text == "":
        comments_label_2 = Label(overall_work_window, text="Work Comments:\n\nNo comments", bg='#121212', fg='green',
                               font=('Times new roman', 30), justify=CENTER).grid(row=1, column=0, columnspan=2, pady=20)
    else:
        comments_label_2 = Label(overall_work_window, text="Work Comments:\n\n%s"%(work_comments_text), bg='#121212',
                               fg='red', font=('Times new roman', 30), justify=CENTER).grid(row=1, column=0, columnspan=2, pady=20)


    global view_work_progress_btn
    view_work_progress_btn = Button(overall_work_window, text="View progress", bg='#121212', fg='white', font=('Arial bold', 15),
                                command=view_work_progress, width=30)
    view_work_progress_btn.grid(row=2, column=0, columnspan=3, pady=20)

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

def view_work_progress():
    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    #get values from database
    c.execute('SELECT Overall_work, oid FROM Work')
    overall_work_list = []
    week_list = []
    data = c.fetchall()

    for row in data:
        overall_work_list.append(row[0])
        week_list.append(row[1])


    plt.plot(week_list, overall_work_list, label = 'Overall Work Score',
      color='blue', marker='o', markerfacecolor='k',
      linestyle='-', linewidth=3)
    plt.xlabel('Week No.')
    plt.ylabel('Overall work performance')
    plt.legend(loc='lower right')
    plt.title('Work Performance(overtime)')
    plt.xticks(week_list)
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    plt.show()

    view_work_progress_btn['state'] = DISABLED
    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

#-----------------------------------------------------------------------------------------------------------------------

def school():
    school_period = True
    global school_window

    # moves to top of canvas
    my_canvas.yview_moveto('0.0')

    # Create frame within canvas
    school_window = Frame(my_canvas, bg='#121212', width=w, height=h, relief=FLAT)

    # Add new frame to window in canvas
    my_canvas.create_window((0, 0), window=school_window, anchor="nw")
    # work_window.place(x=0, y=0)

    # School labels
    global hours_studied_label
    global academic_practice_label
    global school_projects_label
    global assignments_label
    global attachment_label

    # School entries
    global hours_studied_entry
    global academic_practice_entry
    global school_projects_entry
    global assignments_entry
    global attachment_entry

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    school_window_label = Label(school_window, text="School Window.", bg='#121212', fg='white', font=('Times New Roman bold', 30), justify="center").grid(row=0, column=0, columnspan=4, padx=0, pady=10)

    # Creating School Table and if it exists connects cursor
    c.execute("""CREATE TABLE IF NOT EXISTS
               School(
                   Date TEXT PRIMARY KEY,
                   Hours_studied FLOAT,
                   Academic_practice TEXT,
                   School_projects TEXT,
                   Assignments TEXT,
                   Attachment TEXT,
                   Total_school FLOAT,
                   Overall_school FLOAT
               )
           """)

    # ask work questions
    hours_studied_label = Label(school_window, text="How many hours have you studied your courses this week?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=1, column=0, padx=20, pady=20)
    academic_practice_label = Label(school_window, text="Have you done any question papers, involving the courses you are doing?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=2, column=0, padx=20, pady=20)
    school_projects_label = Label(school_window, text="Have you completed or progressed through any school projects you are currently assigned to?\n(Tick \"NONE\" if you do not have any projects): ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=3, column=0, padx=20, pady=20)
    assignments_label = Label(school_window, text="Have you completed any assignments you are currently assigned to?\n(Tick \"NONE\" if you do not have any assignments): ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=4, column=0, padx=20, pady=20)
    attachment_label = Label(school_window, text="Have you found a place for attachment?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=5, column=0, padx=20, pady=20)

    hours_studied_entry = Entry(school_window, width=20, font=('Times New Roman bold', 15))
    hours_studied_entry.grid(row=1, column=1, ipady=15, padx=20, pady=20)

    academic_practice_entry = IntVar()
    academic_practice_entry.set('None')
    global academic_practice_button_1
    global academic_practice_button_2
    academic_practice_button_1 = Radiobutton(school_window, text="Yes", variable=academic_practice_entry, value=1)
    academic_practice_button_1.grid(row=2, column=1)
    academic_practice_button_2 = Radiobutton(school_window, text="No", variable=academic_practice_entry, value=-1)
    academic_practice_button_2.grid(row=2, column=2)

    school_projects_entry = IntVar()
    school_projects_entry.set('None')
    global school_projects_button_1
    global school_projects_button_2
    global school_projects_button_3
    school_projects_button_1 = Radiobutton(school_window, text="Yes", variable=school_projects_entry, value=values[2])
    school_projects_button_1.grid(row=3, column=1)
    school_projects_button_2 = Radiobutton(school_window, text="No", variable=school_projects_entry, value=values[0])
    school_projects_button_2.grid(row=3, column=2)
    school_projects_button_3 = Radiobutton(school_window, text="None", variable=school_projects_entry, value=values[1])
    school_projects_button_3.grid(row=3, column=3, padx=50)

    assignments_entry = IntVar()
    assignments_entry.set('None')
    global assignments_button_1
    global assignments_button_2
    global assignments_button_3
    assignments_button_1 = Radiobutton(school_window, text="Yes", variable=assignments_entry, value=values[2])
    assignments_button_1.grid(row=4, column=1)
    assignments_button_2 = Radiobutton(school_window, text="No", variable=assignments_entry, value=values[0])
    assignments_button_2.grid(row=4, column=2)
    assignments_button_3 = Radiobutton(school_window, text="None", variable=assignments_entry, value=values[1])
    assignments_button_3.grid(row=4, column=3, padx=50)

    attachment_entry = IntVar()
    attachment_entry.set('None')
    global attachment_button_1
    global attachment_button_2
    attachment_button_1 = Radiobutton(school_window, text="Yes", variable=attachment_entry, value=1)
    attachment_button_1.grid(row=5, column=1)
    attachment_button_2 = Radiobutton(school_window, text="No", variable=attachment_entry, value=-1)
    attachment_button_2.grid(row=5, column=2)

    global view_school_btn
    global submit_school_btn
    submit_school_btn = Button(school_window, text="Submit", bg='#121212', fg='white', font=('Arial bold', 15),
                             command=submit_school_info, width=30)
    submit_school_btn.grid(row=6, column=0, columnspan=3, pady=20)
    view_school_btn = Button(school_window, text="View Data", bg='#121212', fg='white', font=('Arial bold', 15),
                           command=view_school_info, width=30)
    view_school_btn.grid(row=7, column=0, columnspan=3, pady=20)
    view_school_btn['state'] = DISABLED

    global close_school_btn
    close_school_btn = Button(school_window, text="Close Table", relief=RAISED, font=('Arial bold', 15),
                            command=close_school_table, width=20)
    close_school_btn.grid(row=9, column=0, columnspan=2, pady=20, padx=(150, 0))
    close_school_btn['state'] = DISABLED

    global view_sch_performance
    view_sch_performance = Button(school_window, text="View Peformance", bg='#121212', fg='white',
                                  font=('Arial bold', 15), command=view_school_performance, width=30)
    view_sch_performance['state'] = DISABLED
    view_sch_performance.grid(row=10, column=0, columnspan=3, pady=20)

    global open_overall_school_btn
    open_overall_school_btn = Button(school_window, text="View Result", bg='#121212', fg='white',
                                   font=('Arial bold', 15), command=overall_school_page, width=30)
    open_overall_school_btn['state'] = DISABLED
    open_overall_school_btn.grid(row=11, column=0, columnspan=3, pady=20)

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()

    return

def submit_school_info():
    # School
    global hours_studied
    global academic_practice
    global school_projects
    global assignments
    global attachment

    #School radio database entries
    global academic_practice_database_entry
    global school_projects_database_entry
    global assignments_database_entry
    global attachment_database_entry

#-----------------------------------------------------------------------------------------------------------------------

    try:
        hours_studied = float(hours_studied_entry.get())
    except ValueError:
        hours_studied_entry.config(bg="Red")
        messagebox.showinfo("", "You entered a string in the box highlighted in red. Please enter a number.")
        hours_studied_entry.delete(0, END)

    hours_studied = float(hours_studied_entry.get())

    while (hours_studied > 100) or (hours_studied < 0):
        hours_studied_entry.config(bg="Red")
        messagebox.showinfo("",
                            "You cannot exceed 100 or subceed 0 study hours in a week. Re-enter a POSITIVE value equal to, or less than 100 in the box highlighted in red.")
        hours_studied_entry.delete(0, END)
        hours_studied = float(hours_studied_entry.get())
    hours_studied_entry.config(bg="White")

#-----------------------------------------------------------------------------------------------------------------------

    try:
        academic_practice = academic_practice_entry.get()
    except TclError:
        academic_practice_button_1.config(bg="Red")
        academic_practice_button_2.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if academic_practice == 1:
        academic_practice_database_entry = "Yes"
    else:
        academic_practice_database_entry = "No"

#-----------------------------------------------------------------------------------------------------------------------

    try:
        school_projects = school_projects_entry.get()
    except TclError:
        school_projects_button_1.config(bg="Red")
        school_projects_button_2.config(bg="Red")
        school_projects_button_3.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if school_projects == 1:
        school_projects_database_entry = "Yes"
    elif school_projects == -1:
        school_projects_database_entry = "No"
    else:
        school_projects_database_entry = "None"

#-----------------------------------------------------------------------------------------------------------------------

    try:
        assignments = assignments_entry.get()
    except TclError:
        assignments_button_1.config(bg="Red")
        assignments_button_2.config(bg="Red")
        assignments_button_3.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if assignments == 1:
        assignments_database_entry = "Yes"
    elif assignments == -1:
        assignments_database_entry = "No"
    else:
        assignments_database_entry = "None"

#-----------------------------------------------------------------------------------------------------------------------

    try:
        attachment = attachment_entry.get()
    except TclError:
        attachment_button_1.config(bg="Red")
        attachment_button_2.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if attachment == 1:
        attachment_database_entry = "Yes"
    else:
        attachment_database_entry = "No"

#-----------------------------------------------------------------------------------------------------------------------

    global total_school
    global overall_school
    total_school = float(hours_studied) + float(academic_practice) + float(school_projects) + float(assignments) + float(attachment)
    x = (float(total_general) + float(total_school)) / 12
    overall_school = float("{:.2f}".format(x))

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # Add values to database
    # Insert into table
    c.execute(
        "INSERT INTO School VALUES(:date, :hours_studied, :academic_practice, :school_projects, :assignments, :attachment, :total_school, :overall_school)",
        {
            'date': current_time,
            'hours_studied': hours_studied,
            'academic_practice': academic_practice_database_entry,
            'school_projects': school_projects_database_entry,
            'assignments': assignments_database_entry,
            'attachment': attachment_database_entry,
            'total_school': total_school,
            'overall_school': overall_school
        })

    academic_practice_button_1.config(bg="White")
    academic_practice_button_2.config(bg="White")

    school_projects_button_1.config(bg="White")
    school_projects_button_2.config(bg="White")
    school_projects_button_3.config(bg="White")

    assignments_button_1.config(bg="White")
    assignments_button_2.config(bg="White")
    assignments_button_3.config(bg="White")

    attachment_button_1.config(bg="White")
    attachment_button_2.config(bg="White")

    messagebox.showinfo("", "Your data has been submitted.")

    # Clear Boxes
    # clear the text boxes
    hours_studied_entry.delete(0, END)
    academic_practice_entry.set('None')
    school_projects_entry.set('None')
    assignments_entry.set('None')
    attachment_entry.set('None')

    view_sch_performance['state'] = NORMAL
    view_school_btn['state'] = NORMAL
    submit_school_btn['state'] = DISABLED

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()

    return

def view_school_info():
    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # Present table
    # Query the database
    c.execute("SELECT *, oid FROM School")
    records = c.fetchall()

    # Add style for treeview
    style = ttk.Style()
    style.theme_use('default')

    # configure treeview colours
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="Black",
                    rowheight=30,
                    fieldbackground="#D3D3D3")

    # Change selected colour
    style.map('Treeview',
              background=[('selected', "#347083")]
              )

    # Create a Treeview frame
    global tree_frame_school
    tree_frame_school = Frame(school_window)
    tree_frame_school.grid(row=8, column=0, columnspan=10, pady=50)

    # Create a Treeview scrollbar
    tree_scroll_school = Scrollbar(tree_frame_school)
    tree_scroll_school.grid(row=0, column=1, sticky=NS)

    # Create treeview
    school_tree = ttk.Treeview(tree_frame_school, yscrollcommand=tree_scroll_school.set, selectmode="extended")
    school_tree.grid(row=0, column=0)

    # Configure scrollbar
    tree_scroll_school.config(command=school_tree.yview)

    # Define columns
    school_tree['columns'] = (
    "Date", "Hours Studied", "Academic Practice", "School Projects", "Assignments", "Attachment", "Total School Score", "Overall School Score", "Week No.")

    # Format columns
    school_tree.column("#0", width=0, stretch=NO)
    school_tree.column("Date", anchor=W, width=140)
    school_tree.column("Hours Studied", anchor=CENTER, width=100)
    school_tree.column("Academic Practice", anchor=CENTER, width=120)
    school_tree.column("School Projects", anchor=CENTER, width=100)
    school_tree.column("Assignments", anchor=CENTER, width=100)
    school_tree.column("Attachment", anchor=CENTER, width=100)
    school_tree.column("Total School Score", anchor=CENTER, width=140)
    school_tree.column("Overall School Score", anchor=CENTER, width=140)
    school_tree.column("Week No.", anchor=CENTER, width=100)

    # Create headings
    school_tree.heading("#0", text="", anchor=CENTER)
    school_tree.heading("Date", text="Date", anchor=CENTER)
    school_tree.heading("Hours Studied", text="Hours Studied", anchor=CENTER)
    school_tree.heading("Academic Practice", text="Academic Practice", anchor=CENTER)
    school_tree.heading("School Projects", text="Projects", anchor=CENTER)
    school_tree.heading("Assignments", text="Assignments", anchor=CENTER)
    school_tree.heading("Attachment", text="Attachment", anchor=CENTER)
    school_tree.heading("Total School Score", text="Total School Score", anchor=CENTER)
    school_tree.heading("Overall School Score", text="Overall School Score", anchor=CENTER)
    school_tree.heading("Week No.", text="Week No.", anchor=CENTER)

    # Create Stripped Row tags
    school_tree.tag_configure('oddrow', background="white")
    school_tree.tag_configure('evenrow', background="light blue")

    # Add data to screen
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            school_tree.insert(parent='', index='end', iid=count, text='', value=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]), tags=('evenrow',))
        else:
            school_tree.insert(parent='', index='end', iid=count, text='', value=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]), tags=('oddrow',))
        # increment counter
        count += 1

    close_school_btn['state'] = NORMAL
    view_school_btn['state'] = DISABLED

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

def close_school_table():
    tree_frame_school.destroy()
    close_school_btn['state'] = DISABLED
    view_school_btn['state'] = NORMAL
    return

def view_school_performance():
    view_sch_performance.destroy()
    if total_school == 14:
        school_performance = Label(school_window, text="Average", bg='#D53600', fg='Black', font=('Arial bold', 15),
                                 relief=SUNKEN).grid(row=10, column=0, padx=0, pady=20)
    elif total_school < 14:
        school_performance = Label(school_window, text="Unsatisfactory", bg='Dark Red', fg='Black',
                                 font=('Arial bold', 15), relief=SUNKEN).grid(row=10, column=0, padx=0, pady=20)
    elif total_school > 14:
        school_performance = Label(school_window, text="Magnificent", bg='Dark Green', fg='Black',
                                 font=('Arial bold', 15), relief=SUNKEN).grid(row=10, column=0, padx=0, pady=20)

    open_overall_school_btn['state'] = NORMAL
    return

def school_comments():
    school_comments = []
    global school_comments_text
    school_comments_text = ""
    if float(hours_studied) < 10:
        school_comments.append("You have to put in more hours of study.\n")
    if academic_practice < 1:
        school_comments.append("Do question papers so you don't have to fail this semester.\n")
    if school_projects == 0:
        school_comments.append("Look for your own personal project to do OR sharpen the skills you already have.\n")
    elif school_projects == -1:
        school_comments.append("Hurry up and finish that project.\n")
    if assignments == 0:
        school_comments.append("Stop sitting around waiting for an assignment and do something.\n")
    elif assignments == -1:
        school_comments.append("Hurry up and finish that assignment.\n")
    if attachment < 1:
        school_comments.append("Hurry up and find a place for attachment.\n")
    if overall_school == 3.375:
        school_comments.append("You are on average. Do better next week.\n")

    for i in range(0, len(school_comments)):
        school_comments_text = school_comments_text + school_comments[i]
        i += 1
    return

def overall_school_page():
    general_comments()
    school_comments()

    school_window.destroy()
    global overall_school_window

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # get values from database
    c.execute('SELECT Overall_school FROM School')
    overall_school_list = []

    data = c.fetchall()

    for row in data:
        overall_school_list.append(row[0])

    index = len(overall_school_list) - 1
    reference = index - 1

    # moves to top of canvas
    my_canvas.yview_moveto('0.0')

    # Create frame within canvas
    overall_school_window = Frame(my_canvas, bg='#121212', width=w, height=h, relief=FLAT)

    # Add new frame to window in canvas
    my_canvas.create_window((0, 0), window=overall_school_window, anchor="nw")

    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        mode="gauge+number+delta",
        value=overall_school_list[index],
        title={'text': "Overall School Performance", 'font': {'size': 20}},
        delta={'reference': overall_school_list[reference]},
        gauge={
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 1.6875], 'color': 'red'},
                {'range': [1.6875, 3.375], 'color': '#D53600'},
                {'range': [3.375, 5.1875], 'color': 'lightgreen'},
                {'range': [5.1875, 7], 'color': 'forestgreen'},
                {'range': [7, 10], 'color': 'darkgreen'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 9}}))

    fig.write_html('School performance.html', auto_open=True)

    if gen_comments_text == "":
        comments_label = Label(overall_school_window, text="General Comments:\n\nNo comments", bg='#121212', fg='green',
                               font=('Times new roman', 30), justify=CENTER).grid(row=0, column=0, columnspan=2,
                                                                                  pady=20)
    else:
        comments_label = Label(overall_school_window, text="General Comments:\n\n%s"%(gen_comments_text), bg='#121212',
                               fg='red', font=('Times new roman', 30), justify=CENTER).grid(row=0, column=0,
                                                                                            columnspan=2, pady=20)

    if school_comments_text == "":
        comments_label_2 = Label(overall_school_window, text="School Comments:\n\nNo comments", bg='#121212', fg='green',
                                 font=('Times new roman', 30), justify=CENTER).grid(row=1, column=0, columnspan=2,
                                                                                    pady=20)
    else:
        comments_label_2 = Label(overall_school_window, text="School Comments:\n\n%s"%(school_comments_text), bg='#121212',
                                 fg='red', font=('Times new roman', 30), justify=CENTER).grid(row=1, column=0,
                                                                                              columnspan=2, pady=20)

    global view_school_progress_btn
    view_school_progress_btn = Button(overall_school_window, text="View progress", bg='#121212', fg='white',
                                    font=('Arial bold', 15),
                                    command=view_school_progress, width=30)
    view_school_progress_btn.grid(row=2, column=0, columnspan=3, pady=20)

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

def view_school_progress():
    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # get values from database
    c.execute('SELECT Overall_school, oid FROM School')
    overall_school_list = []
    week_list = []
    data = c.fetchall()

    for row in data:
        overall_school_list.append(row[0])
        week_list.append(row[1])

    plt.plot(week_list, overall_school_list, label='Overall School Score',
             color='blue', marker='o', markerfacecolor='k',
             linestyle='-', linewidth=3)
    plt.xlabel('Week No.')
    plt.ylabel('Overall school performance')
    plt.legend(loc='lower right')
    plt.title('School Performance(overtime)')
    plt.xticks(week_list)
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.show()

    view_school_progress_btn['state'] = DISABLED
    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

#-----------------------------------------------------------------------------------------------------------------------

def holiday():
    holiday_period = True
    global holiday_window

    # moves to top of canvas
    my_canvas.yview_moveto('0.0')

    # Create frame within canvas
    holiday_window = Frame(my_canvas, bg='#121212', width=w, height=h, relief=FLAT)

    # Add new frame to window in canvas
    my_canvas.create_window((0, 0), window=holiday_window, anchor="nw")
    # work_window.place(x=0, y=0)

    # Work entries
    global media_hours_entry
    global improving_and_learning_entry
    global working_entry

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    holiday_window_label = Label(holiday_window, text="Holiday Window.", bg='#121212', fg='white',
                              font=('Times New Roman bold', 30), justify="center").grid(row=0, column=0, columnspan=4,
                                                                                        padx=0, pady=10)

    # Creating General Table and if it exists connects cursor
    c.execute("""CREATE TABLE IF NOT EXISTS
               Holiday(
                   Date TEXT PRIMARY KEY,
                   Media_hours FLOAT,
                   Improving TEXT,
                   Working TEXT,
                   Total_holiday FLOAT,
                   Overall_holiday FLOAT
               )
           """)

    # ask work questions
    media_hours_label = Label(holiday_window, text="How many hours have you spent practicing your MEDIA skills?: ",
                               bg='#121212',
                               fg='white', font=('Times New Roman bold', 15)).grid(row=1, column=0, padx=20, pady=20)
    improving_and_learning_label = Label(holiday_window, text="Have you been HONING old skills, and/or LEARNING new skills?: ", bg='#121212',
                           fg='white',
                           font=('Times New Roman bold', 15)).grid(row=2, column=0, padx=20, pady=20)
    working_label = Label(holiday_window,
                                text="Have you found some sort of WORK to do during the holiday(either personal or with someone else)?: ",
                                bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=3, column=0,
                                                                                                  padx=20, pady=20)

    media_hours_entry = Entry(holiday_window, width=20, font=('Times New Roman bold', 15))
    media_hours_entry.grid(row=1, column=1, ipady=15, padx=20, pady=20)

    improving_and_learning_entry = IntVar()
    improving_and_learning_entry.set('None')
    global improving_and_learning_button_1
    global improving_and_learning_button_2
    improving_and_learning_button_1 = Radiobutton(holiday_window, text="Yes", variable=improving_and_learning_entry, value=values[2])
    improving_and_learning_button_1.grid(row=2, column=1)
    improving_and_learning_button_2 = Radiobutton(holiday_window, text="No", variable=improving_and_learning_entry, value=values[0])
    improving_and_learning_button_2.grid(row=2, column=2)

    working_entry = IntVar()
    working_entry.set('None')
    global working_button_1
    global working_button_2
    working_button_1 = Radiobutton(holiday_window, text="Yes", variable=working_entry, value=values[2])
    working_button_1.grid(row=3, column=1)
    working_button_2 = Radiobutton(holiday_window, text="No", variable=working_entry, value=values[0])
    working_button_2.grid(row=3, column=2)

    global view_holiday_btn
    global submit_holiday_btn
    submit_holiday_btn = Button(holiday_window, text="Submit", bg='#121212', fg='white', font=('Arial bold', 15),
                             command=submit_holiday_info, width=30)
    submit_holiday_btn.grid(row=4, column=0, columnspan=3, pady=20)
    view_holiday_btn = Button(holiday_window, text="View Data", bg='#121212', fg='white', font=('Arial bold', 15),
                           command=view_holiday_info, width=30)
    view_holiday_btn.grid(row=5, column=0, columnspan=3, pady=20)
    view_holiday_btn['state'] = DISABLED

    global close_holiday_btn
    close_holiday_btn = Button(holiday_window, text="Close Table", relief=RAISED, font=('Arial bold', 15),
                            command=close_holiday_table, width=20)
    close_holiday_btn.grid(row=7, column=0, columnspan=2, pady=20, padx=(60, 0))
    close_holiday_btn['state'] = DISABLED

    global view_hld_performance
    view_hld_performance = Button(holiday_window, text="View Peformance", bg='#121212', fg='white',
                                  font=('Arial bold', 15), command=view_holiday_performance, width=30)
    view_hld_performance['state'] = DISABLED
    view_hld_performance.grid(row=8, column=0, columnspan=3, pady=20)

    global open_overall_holiday_btn
    open_overall_holiday_btn = Button(holiday_window, text="View Result", bg='#121212', fg='white',
                                   font=('Arial bold', 15), command=overall_holiday_page, width=30)
    open_overall_holiday_btn['state'] = DISABLED
    open_overall_holiday_btn.grid(row=9, column=0, columnspan=3, pady=20)

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

def submit_holiday_info():
    global media_hours
    global improving_and_learning
    global working

    # Work radio database entries
    global improving_and_learning_database_entry
    global working_database_entry

#-----------------------------------------------------------------------------------------------------------------------

    try:
        media_hours = float(media_hours_entry.get())
    except ValueError:
        media_hours_entry.config(bg="Red")
        messagebox.showinfo("", "You entered a string in the box highlighted in red. Please enter a number.")
        media_hours_entry.delete(0, END)

    media_hours = float(media_hours_entry.get())

    while (media_hours > 56) or (media_hours < 0):
        media_hours_entry.config(bg="Red")
        messagebox.showinfo("",
                            "You cannot exceed 56 or subceed 0 hours of creative hours in a week. Re-enter a POSITIVE value equal to, or less than 56 in the box highlighted in red.")
        media_hours_entry.delete(0, END)
        media_hours = float(media_hours_entry.get())
    media_hours_entry.config(bg="White")

#-----------------------------------------------------------------------------------------------------------------------

    try:
        improving_and_learning = improving_and_learning_entry.get()
    except TclError:
        improving_and_learning_button_1.config(bg="Red")
        improving_and_learning_button_2.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if improving_and_learning == 1:
        improving_and_learning_database_entry = "Yes"
    else:
        improving_and_learning_database_entry = "No"

#-----------------------------------------------------------------------------------------------------------------------

    try:
        working = working_entry.get()
    except TclError:
        working_button_1.config(bg="Red")
        working_button_2.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if working == 1:
        working_database_entry = "Yes"
    else:
        working_database_entry = "No"

#-----------------------------------------------------------------------------------------------------------------------

    global total_holiday
    global overall_holiday
    total_holiday = float(media_hours) + float(improving_and_learning) + float(working)
    x = (float(total_general) + float(total_holiday)) / 10
    overall_holiday = float("{:.2f}".format(x))

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # Add values to database
    # Insert into table
    c.execute(
        "INSERT INTO Holiday VALUES(:date, :media_hours, :improving_and_learning, :working, :total_holiday, :overall_holiday)",
        {
            'date': current_time,
            'media_hours': media_hours,
            'improving_and_learning': improving_and_learning_database_entry,
            'working': working_database_entry,
            'total_holiday': total_holiday,
            'overall_holiday': overall_holiday
        })

    improving_and_learning_button_1.config(bg="White")
    improving_and_learning_button_2.config(bg="White")

    working_button_1.config(bg="White")
    working_button_2.config(bg="White")

    messagebox.showinfo("", "Your data has been submitted.")

    # Clear Boxes
    # clear the text boxes
    media_hours_entry.delete(0, END)
    improving_and_learning_entry.set('None')
    working_entry.set('None')

    view_hld_performance['state'] = NORMAL
    view_holiday_btn['state'] = NORMAL
    submit_holiday_btn['state'] = DISABLED

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()

    return

def view_holiday_info():
    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # Present table
    # Query the database
    c.execute("SELECT *, oid FROM Holiday")
    records = c.fetchall()

    # Add style for treeview
    style = ttk.Style()
    style.theme_use('default')

    # configure treeview colours
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="Black",
                    rowheight=30,
                    fieldbackground="#D3D3D3")

    # Change selected colour
    style.map('Treeview',
              background=[('selected', "#347083")]
              )

    # Create a Treeview frame
    global tree_frame_holiday
    tree_frame_holiday = Frame(holiday_window)
    tree_frame_holiday.grid(row=6, column=0, columnspan=10, pady=50)

    # Create a Treeview scrollbar
    tree_scroll_holiday = Scrollbar(tree_frame_holiday)
    tree_scroll_holiday.grid(row=0, column=1, sticky=NS)

    # Create treeview
    holiday_tree = ttk.Treeview(tree_frame_holiday, yscrollcommand=tree_scroll_holiday.set, selectmode="extended")
    holiday_tree.grid(row=0, column=0)

    # Configure scrollbar
    tree_scroll_holiday.config(command=holiday_tree.yview)

    # Define columns
    holiday_tree['columns'] = (
    "Date", "Media Hours", "Improving & Learning", "Working", "Total Holiday Score", "Overall Holiday Score", "Week No.")

    # Format columns
    holiday_tree.column("#0", width=0, stretch=NO)
    holiday_tree.column("Date", anchor=W, width=140)
    holiday_tree.column("Media Hours", anchor=CENTER, width=100)
    holiday_tree.column("Improving & Learning", anchor=CENTER, width=140)
    holiday_tree.column("Working", anchor=CENTER, width=100)
    holiday_tree.column("Total Holiday Score", anchor=CENTER, width=140)
    holiday_tree.column("Overall Holiday Score", anchor=CENTER, width=140)
    holiday_tree.column("Week No.", anchor=CENTER, width=100)

    # Create headings
    holiday_tree.heading("#0", text="", anchor=CENTER)
    holiday_tree.heading("Date", text="Date", anchor=CENTER)
    holiday_tree.heading("Media Hours", text="Media Hours", anchor=CENTER)
    holiday_tree.heading("Improving & Learning", text="Improving & Learning?", anchor=CENTER)
    holiday_tree.heading("Working", text="Working?", anchor=CENTER)
    holiday_tree.heading("Total Holiday Score", text="Total Holiday Score", anchor=CENTER)
    holiday_tree.heading("Overall Holiday Score", text="Overall Holiday Score", anchor=CENTER)
    holiday_tree.heading("Week No.", text="Week No.", anchor=CENTER)

    # Create Stripped Row tags
    holiday_tree.tag_configure('oddrow', background="white")
    holiday_tree.tag_configure('evenrow', background="light blue")

    # Add data to screen
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            holiday_tree.insert(parent='', index='end', iid=count, text='', value=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
        else:
            holiday_tree.insert(parent='', index='end', iid=count, text='', value=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',))
        # increment counter
        count += 1

    close_holiday_btn['state'] = NORMAL
    view_holiday_btn['state'] = DISABLED

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

def close_holiday_table():
    tree_frame_holiday.destroy()
    close_holiday_btn['state'] = DISABLED
    view_holiday_btn['state'] = NORMAL
    return

def view_holiday_performance():
    view_hld_performance.destroy()
    if total_holiday == 12:
        holiday_performance = Label(holiday_window, text="Average", bg='#D53600', fg='Black', font=('Arial bold', 15),
                                 relief=SUNKEN).grid(row=8, column=0, padx=0, pady=20)
    elif total_holiday < 12:
        holiday_performance = Label(holiday_window, text="Unsatisfactory", bg='Dark Red', fg='Black',
                                 font=('Arial bold', 15), relief=SUNKEN).grid(row=8, column=0, padx=0, pady=20)
    elif total_holiday > 12:
        holiday_performance = Label(holiday_window, text="Magnificent", bg='Dark Green', fg='Black',
                                 font=('Arial bold', 15), relief=SUNKEN).grid(row=8, column=0, padx=0, pady=20)

    open_overall_holiday_btn['state'] = NORMAL
    return

def holiday_comments():
    holiday_comments = []
    global holiday_comments_text
    holiday_comments_text = ""
    if float(media_hours) < 10:
        holiday_comments.append("You have to put in more hours to improve your media skills.\n")
    if improving_and_learning < 1:
        holiday_comments.append("Learn something valuable this week AND/OR sharpen the skills you currently have.\n")
    if working < 1:
        holiday_comments.append("Look for your own personal project to do OR assist anyone you know in their project.\n")
    if overall_holiday == 3.375:
        holiday_comments.append("You are on average. Do better next week.\n")

    for i in range(0, len(holiday_comments)):
        holiday_comments_text = holiday_comments_text + holiday_comments[i]
        i += 1
    return

def overall_holiday_page():
    general_comments()
    holiday_comments()

    holiday_window.destroy()
    global overall_holiday_window

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # get values from database
    c.execute('SELECT Overall_holiday FROM Holiday')
    overall_holiday_list = []

    data = c.fetchall()

    for row in data:
        overall_holiday_list.append(row[0])

    index = len(overall_holiday_list) - 1
    reference = index - 1

    # moves to top of canvas
    my_canvas.yview_moveto('0.0')

    # Create frame within canvas
    overall_holiday_window = Frame(my_canvas, bg='#121212', width=w, height=h, relief=FLAT)

    # Add new frame to window in canvas
    my_canvas.create_window((0, 0), window=overall_holiday_window, anchor="nw")

    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        mode="gauge+number+delta",
        value=overall_holiday_list[index],
        title={'text': "Overall Holiday Performance", 'font': {'size': 20}},
        delta={'reference': overall_holiday_list[reference]},
        gauge={
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 1.9255], 'color': 'red'},
                {'range': [1.925, 3.85], 'color': '#D53600'},
                {'range': [3.85, 5.425], 'color': 'lightgreen'},
                {'range': [5.425, 7], 'color': 'forestgreen'},
                {'range': [7, 10], 'color': 'darkgreen'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 9}}))


    fig.write_html('Holiday performance.html', auto_open=True)

    if gen_comments_text == "":
        comments_label = Label(overall_holiday_window, text="General Comments:\n\nNo comments", bg='#121212', fg='green',
                               font=('Times new roman', 30), justify=CENTER).grid(row=0, column=0, columnspan=2,
                                                                                  pady=20)
    else:
        comments_label = Label(overall_holiday_window, text="General Comments:\n\n%s"%(gen_comments_text),
                               bg='#121212',
                               fg='red', font=('Times new roman', 25), justify=CENTER).grid(row=0, column=0,
                                                                                            columnspan=2, pady=20)

    if holiday_comments_text == "":
        comments_label_2 = Label(overall_holiday_window, text="Holiday Comments:\n\nNo comments", bg='#121212', fg='green',
                                 font=('Times new roman', 30), justify=CENTER).grid(row=1, column=0, columnspan=2,
                                                                                    pady=20)
    else:
        comments_label_2 = Label(overall_holiday_window, text="Holiday Comments:\n\n%s"%(holiday_comments_text),
                                 bg='#121212',
                                 fg='red', font=('Times new roman', 25), justify=CENTER).grid(row=1, column=0, columnspan=2, pady=20)

    global view_holiday_progress_btn
    view_holiday_progress_btn = Button(overall_holiday_window, text="View progress", bg='#121212', fg='white',
                                      font=('Arial bold', 15),
                                      command=view_holiday_progress, width=30)
    view_holiday_progress_btn.grid(row=2, column=0, columnspan=3, pady=20)

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

def view_holiday_progress():
    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # get values from database
    c.execute('SELECT Overall_holiday, oid FROM Holiday')
    overall_holiday_list = []
    week_list = []
    data = c.fetchall()

    for row in data:
        overall_holiday_list.append(row[0])
        week_list.append(row[1])

    plt.plot(week_list, overall_holiday_list, label='Overall Holiday Score',
             color='blue', marker='o', markerfacecolor='k',
             linestyle='-', linewidth=3)
    plt.xlabel('Week No.')
    plt.ylabel('Overall Holiday performance')
    plt.legend(loc='lower right')
    plt.title('Holiday Performance(overtime)')
    plt.xticks(week_list)
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.show()

    view_holiday_progress_btn['state'] = DISABLED
    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()
    return

#-----------------------------------------------------------------------------------------------------------------------

def Continue():
    general_window.destroy()
    period = var.get()

    if period == "School":
        school()
    elif period == "Work":
        work()
    elif period == "Holiday":
        holiday()

def selected(event):
    continue_btn['state'] = NORMAL

def select_period():
    global var
    global period
    var = StringVar()
    var.set("Period")

    # Drop down menu
    global options
    options = [
        "School",
        "Work",
        "Holiday"
    ]

    var.set("Period")
    helv36 = tkFont.Font(family='Helvetica', size=20)
    drop = OptionMenu(general_window, var, *options, command=selected)
    drop.config(font=helv36)
    drop.grid(row=14, column=1, padx=0, pady=20, ipadx=20, ipady=20)

    global continue_btn
    continue_btn = Button(general_window, text="Continue", command=Continue, font=('Arial bold', 15), width=50,
                          bg="Black", fg="White")
    continue_btn.grid(row=15, column=0, columnspan=4, padx=0, pady=50)
    continue_btn['state'] = DISABLED

#-----------------------------------------------------------------------------------------------------------------------

def general():
    global general_window

    # moves to top of canvas
    my_canvas.yview_moveto('0.0')

    # Create frame in my_canvas
    general_window = Frame(my_canvas, bg='#121212', width=w, height=h, relief=FLAT)


    # Add new frame to window in canvas
    my_canvas.create_window((0, 0), window=general_window, anchor="nw")

    # General entries
    global gym_attendance_entry
    global shoe_sales_entry
    global hours_honing_entry
    global financial_learning_entry
    global personal_projects_radio_entry
    global book_reading_entry
    global financial_statement_radio_entry

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    general_window_label = Label(general_window, text="General Window.", bg='#121212', fg='white', font=('Times New Roman bold', 30), justify="center").grid(row=0, column=0, columnspan=4, padx=0, pady=10)

    #Creating General Table and if it exists connects corsor
    c.execute("""CREATE TABLE IF NOT EXISTS
        General(
            Date TEXT PRIMARY KEY,
            Gym_attendance INTEGER,
            Sales INTEGER,
            Hours_honing FLOAT,
            Financial_learning FLOAT,
            Personal_projects TEXT,
            Book_reading INTEGER,
            Financial_statement TEXT,
            Total_general FLOAT
        )
    """)

    #Asks general qsns
    gym_attendance_label = Label(general_window, text="How many times did you go to the gym this week?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=1, column=0, padx=10, pady=10)
    shoe_sales_label = Label(general_window, text="How many items did you sell this week?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=2, column=0, padx=10, pady=10)
    hours_honing_label = Label(general_window, text="How many hours have you spent honing old & gaining new skills?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=3, column=0, padx=10, pady=10)
    financial_learning_label = Label(general_window, text="How many hours have you spent on financial education?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=4, column=0, padx=10, pady=10)
    personal_projects_label = Label(general_window, text="Have you done and/or completed your own project?(If you have no projects click \"NONE\") : ", bg='#121212', fg='white', font=('Times New Roman bold', 15), justify="left").grid(row=5, column=0, padx=10, pady=10)
    book_reading_label = Label(general_window, text="How many chapters of a book you are currently reading have you read(and understood) this week?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=6, column=0, padx=10, pady=10)
    financial_statement_label = Label(general_window, text="Have you drawn the financial statement for this week?: ", bg='#121212', fg='white', font=('Times New Roman bold', 15)).grid(row=7, column=0, padx=10, pady=10)


    #Entering answers to questions and storing values in variables
    gym_attendance_entry = Entry(general_window, width=20, font=('Times New Roman bold', 15))
    gym_attendance_entry.grid(row=1, column=1, ipady=15, padx=10, pady=10)
    shoe_sales_entry = Entry(general_window, width=20, font=('Times New Roman bold', 15))
    shoe_sales_entry.grid(row=2, column=1, ipady=15, padx=10, pady=10)
    hours_honing_entry = Entry(general_window, width=20, font=('Times New Roman bold', 15))
    hours_honing_entry.grid(row=3, column=1, ipady=15, padx=10, pady=10)
    financial_learning_entry = Entry(general_window, width=20, font=('Times New Roman bold', 15))
    financial_learning_entry.grid(row=4, column=1, ipady=15, padx=10, pady=10)

    personal_projects_radio_entry = IntVar()
    personal_projects_radio_entry.set('None')
    global personal_projects_button_1
    global personal_projects_button_2
    global personal_projects_button_3
    personal_projects_button_1 = Radiobutton(general_window, text="Yes", variable=personal_projects_radio_entry, value=values[2])
    personal_projects_button_1.grid(row=5, column=1)
    personal_projects_button_2 = Radiobutton(general_window, text="No", variable=personal_projects_radio_entry, value=values[0])
    personal_projects_button_2.grid(row=5, column=2)
    personal_projects_button_3 = Radiobutton(general_window, text="None", variable=personal_projects_radio_entry, value=values[1])
    personal_projects_button_3.grid(row=5, column=3, padx=50)

    book_reading_entry = Entry(general_window, width=20, font=('Times New Roman bold', 15))
    book_reading_entry.grid(row=6, column=1, ipady=15, padx=10, pady=10)

    financial_statement_radio_entry = IntVar()
    financial_statement_radio_entry.set('None')
    global financial_statement_button_1
    global financial_statement_button_2
    financial_statement_button_1 = Radiobutton(general_window, text="Yes", variable=financial_statement_radio_entry, value=values[2])
    financial_statement_button_1.grid(row=7, column=1)
    financial_statement_button_2 = Radiobutton(general_window, text="No", variable=financial_statement_radio_entry, value=values[0])
    financial_statement_button_2.grid(row=7, column=2)


    global view_general_btn
    global submit_general_btn
    submit_general_btn = Button(general_window, text="Submit", bg='#121212', fg='white', font=('Arial bold', 15), command=submit_general_info, width=30)
    submit_general_btn.grid(row=8, column=0, columnspan=3, pady=20)
    view_general_btn = Button(general_window, text="View Data", bg='#121212', fg='white', font=('Arial bold', 15), command=view_general_info, width=30)
    view_general_btn.grid(row=9, column=0, columnspan=3, pady=20)
    view_general_btn['state'] = DISABLED


    global close_tree_frame_btn
    close_tree_frame_btn = Button(general_window, text="Close Table", relief=RAISED, font=('Arial bold', 15), width=20,
                                  command=close_tree_frame)
    close_tree_frame_btn.grid(row=11, column=0, columnspan=5, pady=30)
    close_tree_frame_btn['state'] = DISABLED

    global view_general_performance
    view_general_performance = Button(general_window, text="View performance", bg='#121212', fg='white', font=('Arial bold', 15), command=view_gen_perfromance, width=30)
    view_general_performance['state'] = DISABLED
    view_general_performance.grid(row=13, column=0, padx=0, pady=20, columnspan=3)

    select_period_label = Label(general_window, text="Select period: ", bg='#121212', fg='white', font=('Arial', 15), justify="left").grid(row=14, column=0, padx=0, pady=20)
    select_period()

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()

def submit_general_info():
    # General variables
    global gym_attendance
    global shoe_sales
    global hours_honing
    global financial_learning
    global personal_projects
    global book_reading
    global financial_statement

    # General radio database entries
    global personal_projects_database_entry
    global financial_statement_database_entry

    # here we check wether the inputs are valid or not
    try:
        gym_attendance = int(gym_attendance_entry.get())
    except ValueError:
        gym_attendance_entry.config(bg="Red")
        messagebox.showinfo("", "You entered a string in the box highlighted in red. Please enter a number.")
        gym_attendance_entry.delete(0, END)

    gym_attendance = int(gym_attendance_entry.get())

    while (gym_attendance > 7) or (gym_attendance < 0):
        gym_attendance_entry.config(bg="Red")
        messagebox.showinfo("", "You cannot exceed 7 or go less than 0 days at the gym. Re-enter a POSITIVE value equal to, or less than 7 in the box highlighted in red.")
        gym_attendance_entry.delete(0, END)
        gym_attendance = int(gym_attendance_entry.get())
    gym_attendance_entry.config(bg="White")

#-----------------------------------------------------------------------------------------------------------------------
    try:
        shoe_sales = int(shoe_sales_entry.get())
    except ValueError:
        shoe_sales_entry.config(bg="Red")
        messagebox.showinfo("", "You entered a string in the box highlighted in red. Please enter a number.")
        shoe_sales_entry.delete(0, END)

    shoe_sales = int(shoe_sales_entry.get())

    while (shoe_sales > 100) or (shoe_sales < 0):
        shoe_sales_entry.config(bg="Red")
        messagebox.showinfo("", "You cannot exceed selling 100 or sell less than 0 shoes in a week. Re-enter a POSITIVE value equal to, or less than 100 in the box highlighted in red.")
        shoe_sales_entry.delete(0, END)
        shoe_sales = int(shoe_sales_entry.get())
    shoe_sales_entry.config(bg="White")

# -----------------------------------------------------------------------------------------------------------------------
    try:
        hours_honing = float(hours_honing_entry.get())
    except ValueError:
        hours_honing_entry.config(bg="Red")
        messagebox.showinfo("", "You entered a string in the box highlighted in red. Please enter a number.")
        hours_honing_entry.delete(0, END)

    hours_honing = float(hours_honing_entry.get())

    while (hours_honing > 56) or (hours_honing < 0):
        hours_honing_entry.config(bg="Red")
        messagebox.showinfo("", "You cannot exceed 56 or subceed 0 hours of honing your skills in a week. Re-enter a POSITIVE value equal to, or less than 56 in the box highlighted in red.")
        hours_honing_entry.delete(0, END)
        hours_honing = float(hours_honing_entry.get())
    hours_honing_entry.config(bg="White")

# -----------------------------------------------------------------------------------------------------------------------
    try:
        financial_learning = float(financial_learning_entry.get())
    except ValueError:
        financial_learning_entry.config(bg="Red")
        messagebox.showinfo("", "You entered a string in the box highlighted in red. Please enter a number.")
        financial_learning_entry.delete(0, END)

    financial_learning = float(financial_learning_entry.get())

    while (financial_learning > 56) or (financial_learning < 0):
        financial_learning_entry.config(bg="Red")
        messagebox.showinfo("", "You cannot exceed 56 or subceed 0 hours of learning finances in a week. Re-enter a POSITIVE value equal to, or less than 56 in the box highlighted in red.")
        financial_learning_entry.delete(0, END)
        financial_learning = float(financial_learning_entry.get())
    financial_learning_entry.config(bg="White")

# -----------------------------------------------------------------------------------------------------------------------
    try:
        personal_projects = personal_projects_radio_entry.get()
    except TclError:
        personal_projects_button_1.config(bg="Red")
        personal_projects_button_2.config(bg="Red")
        personal_projects_button_3.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if personal_projects == 1:
        personal_projects_database_entry = "Yes"
    elif personal_projects == -1:
        personal_projects_database_entry = "No"
    else:
        personal_projects_database_entry = "None"

# -----------------------------------------------------------------------------------------------------------------------
    try:
        book_reading = int(book_reading_entry.get())
    except ValueError:
        book_reading_entry.config(bg="Red")
        messagebox.showinfo("", "You entered a string in the box highlighted in red. Please enter a number.")
        book_reading_entry.delete(0, END)

    book_reading = int(book_reading_entry.get())

    while (book_reading > 100) or (book_reading < 0):
        book_reading_entry.config(bg="Red")
        messagebox.showinfo("", "You cannot exceed 100 or read less than 0 chapters of a book in a week. Re-enter a POSITIVE value equal to, or less than 100 in the box highlighted in red.")
        book_reading_entry.delete(0, END)
        book_reading = int(book_reading_entry.get())
    book_reading_entry.config(bg="White")

# -----------------------------------------------------------------------------------------------------------------------
    try:
        financial_statement = financial_statement_radio_entry.get()
    except TclError:
        financial_statement_button_1.config(bg="Red")
        financial_statement_button_2.config(bg="Red")
        messagebox.showinfo("", "Click ANY of the buttons highlighted in red")

    if financial_statement == 1:
        financial_statement_database_entry = "Yes"
    else:
        financial_statement_database_entry = "No"

# -----------------------------------------------------------------------------------------------------------------------
    global total_general
    total_general = float(gym_attendance) + float(shoe_sales) + float(hours_honing) + float(financial_learning) + float(
        personal_projects) + float(book_reading) + float(financial_statement)

    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # Add values to database
    # Insert into table
    c.execute(
        "INSERT INTO General VALUES (:date, :gym_attendance, :sales, :hours_honing, :financial_learning, :personal_projects, :book_reading, :financial_statement, :total_general)",
        {
            'date': current_time,
            'gym_attendance': gym_attendance,
            'sales': shoe_sales,
            'hours_honing': hours_honing,
            'financial_learning': financial_learning,
            'personal_projects': personal_projects_database_entry,
            'book_reading': book_reading,
            'financial_statement': financial_statement_database_entry,
            'total_general': total_general
        })

    personal_projects_button_1.config(bg="White")
    personal_projects_button_2.config(bg="White")
    personal_projects_button_3.config(bg="White")

    financial_statement_button_1.config(bg="White")
    financial_statement_button_2.config(bg="White")

    messagebox.showinfo("", "Your data has been submitted.")

    # Clear Boxes
    # clear the text boxes
    gym_attendance_entry.delete(0, END)
    shoe_sales_entry.delete(0, END)
    hours_honing_entry.delete(0, END)
    financial_learning_entry.delete(0, END)
    personal_projects_radio_entry.set('None')
    book_reading_entry.delete(0, END)
    financial_statement_radio_entry.set('None')

    view_general_performance['state'] = NORMAL
    view_general_btn['state'] = NORMAL
    submit_general_btn['state'] = DISABLED

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()

def view_general_info():
    # Create/connect to database
    conn = sqlite3.connect("Performance_Database.db")

    # Create cursor
    c = conn.cursor()

    # Present table
    # Query the database
    c.execute("SELECT *, oid FROM General")
    records = c.fetchall()

    #Add style for treeview
    style = ttk.Style()
    style.theme_use('default')

    #configure treeview colours
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="Black",
                    rowheight=30,
                    fieldbackground="#D3D3D3")

    #Change selected colour
    style.map('Treeview',
              background=[('selected', "#347083")]
              )

    #Create a Treeview frame
    global tree_frame_gen
    tree_frame_gen = Frame(general_window)
    tree_frame_gen.grid(row=10, column=0, columnspan=10, pady=50)



    #Create a Treeview scrollbar
    tree_scroll_gen = Scrollbar(tree_frame_gen)
    tree_scroll_gen.grid(row=0, column=1, sticky=NS)

    #Create treeview
    global gen_tree
    gen_tree = ttk.Treeview(tree_frame_gen, yscrollcommand=tree_scroll_gen.set, selectmode="extended")
    gen_tree.grid(row=0, column=0)

    #Configure scrollbar
    tree_scroll_gen.config(command=gen_tree.yview)

    #Define columns
    gen_tree['columns'] = ("Date", "Gym Days", "Shoe Sales", "Hours Honing", "Financial learning Time", "Personal Projects", "Book Chapters", "Financial Statement", "Total General Score", "Week No.")

    #Format columns
    gen_tree.column("#0", width=0, stretch=NO)
    gen_tree.column("Date", anchor=W, width=140)
    gen_tree.column("Gym Days", anchor=CENTER, width=100)
    gen_tree.column("Shoe Sales", anchor=CENTER, width=100)
    gen_tree.column("Hours Honing", anchor=CENTER, width=140)
    gen_tree.column("Financial learning Time", anchor=CENTER, width=140)
    gen_tree.column("Personal Projects", anchor=CENTER, width=100)
    gen_tree.column("Book Chapters", anchor=CENTER, width=140)
    gen_tree.column("Financial Statement", anchor=CENTER, width=120)
    gen_tree.column("Total General Score", anchor=CENTER, width=140)
    gen_tree.column("Week No.", anchor=CENTER, width=100)

    #Create headings
    gen_tree.heading("#0", text="", anchor=CENTER)
    gen_tree.heading("Date", text="Date", anchor=CENTER)
    gen_tree.heading("Gym Days", text="Gym Days", anchor=CENTER)
    gen_tree.heading("Shoe Sales", text="Sales", anchor=CENTER)
    gen_tree.heading("Hours Honing", text="Hours Honing", anchor=CENTER)
    gen_tree.heading("Financial learning Time", text="Financial learning Time", anchor=CENTER)
    gen_tree.heading("Personal Projects", text="Personal Projects?", anchor=CENTER)
    gen_tree.heading("Book Chapters", text="Book Chapters", anchor=CENTER)
    gen_tree.heading("Financial Statement", text="Financial Statement?", anchor=CENTER)
    gen_tree.heading("Total General Score", text="Total General Score", anchor=CENTER)
    gen_tree.heading("Week No.", text="Week No.", anchor=CENTER)

    #Create Stripped Row tags
    gen_tree.tag_configure('oddrow', background="white")
    gen_tree.tag_configure('evenrow', background="light blue")

    #Add data to screen
    global count
    count = 0
    for record in records:
        if count%2 == 0:
            gen_tree.insert(parent='', index='end', iid=count, text='', value=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=('evenrow',))
        else:
            gen_tree.insert(parent='', index='end', iid=count, text='', value=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8],record[9]), tags=('oddrow',))
        #increment counter
        count += 1

    close_tree_frame_btn['state'] = NORMAL
    view_general_btn['state'] = DISABLED

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()

def view_gen_perfromance():
    view_general_performance.destroy()
    if total_general == 26.5:
        gen_perfromance = Label(general_window, text="Average", bg='#D53600', fg='Black', font=('Arial bold', 15), relief=SUNKEN).grid(row=12, column=0, padx=0, pady=20)
    elif total_general < 26.5:
        gen_perfromance = Label(general_window, text="Unsatisfactory", bg='Dark Red', fg='Black', font=('Arial bold', 15), relief=SUNKEN).grid(row=12, column=0, padx=0, pady=20)
    elif total_general > 26.5:
        gen_perfromance = Label(general_window, text="Magnificent", bg='Dark Green', fg='Black', font=('Arial bold', 15), relief=SUNKEN).grid(row=12, column=0, padx=0, pady=20)

def general_comments():
    gen_comments = []
    global gen_comments_text
    gen_comments_text = ""
    if float(gym_attendance) < 5:
        gen_comments.append("You need to go to the gym more.\n")
    if float(shoe_sales) < 5:
        gen_comments.append("You need to sell more items.\n")
    if float(hours_honing) < 5:
        gen_comments.append("You need to spend more time honing your skills.\n")
    if float(financial_learning) < 2.5:
        gen_comments.append("You need to spend more time learning about finances.\n")
    if personal_projects == 0:
        gen_comments.append("Find a project to do.\n")
    elif personal_projects == -1:
        gen_comments.append("Hurry up and complete that project.\n")
    if float(book_reading) < 7:
        gen_comments.append("You need to read more books/novels/guides/etc.\n")
    if financial_statement < 1:
        gen_comments.append("Go and prepare a financial statement for the week.\n")
    if total_general == 26.5:
        gen_comments.append("You are on average. Do better next week.\n")

    for i in range(0, len(gen_comments)):
        gen_comments_text = gen_comments_text + gen_comments[i]
        i += 1
    return

def close_tree_frame():
    tree_frame_gen.destroy()
    close_tree_frame_btn['state'] = DISABLED
    view_general_btn['state'] = NORMAL

#-----------------------------------------------------------------------------------------------------------------------


root = Tk()
root.title("Performance")
root.state("zoomed")
root.iconbitmap('C:/Users/Codex/PycharmProjects/tkinter practice/images/icon.ico')
#root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='C:/Users/Codex/PycharmProjects/tkinter practice/images/original.jpg'))
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.geometry("%dx%d" % (w, h))
#root.attributes('-fullscreen', True)
#root.resizable(False, False)
root.configure(bg='#121212') #to change the window color

#Create a main frame
main_frame = Frame(root, bg='#121212', bd=5, relief=SUNKEN)
main_frame.place(x=0, y=0)
main_frame.pack(fill=BOTH, expand=1)

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


#For use during program

school_period = False
work_period = False
holiday_period = False

values = [-1, 0, 1]

current_time = str(time.asctime())

#Create/connect to database
conn = sqlite3.connect("Performance_Database.db")

#Create cursor
c = conn.cursor()

# Creating a canvas
my_canvas = Canvas(main_frame, bg='#121212', width=w, height=h, scrollregion=(0, 0, (w*2), (h*2)), bd=5, highlightbackground="#121212", highlightcolor="#121212")

# Add a scrollbar to canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL)
my_scrollbar.pack(side=RIGHT, fill=Y)
my_scrollbar.config(command=my_canvas.yview)
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
my_canvas.bind_all("<MouseWheel>", OnMouseWheel)

start_window = Frame(my_canvas, bg='#121212', width=w, height=h, relief=FLAT)
global password_entry

# Add new frame to window in canvas
my_canvas.create_window((0, 0), window=start_window, anchor="nw")
my_canvas.grid_rowconfigure(0, weight=1)
my_canvas.grid_columnconfigure(0, weight=1)
start_label = Label(start_window, text="Hello User", bg='#121212', fg='white', font=('Times New Roman bold', 60), justify="center").grid(row=0, column=0, columnspan=20, ipadx=20, ipady=40, pady=40, sticky="")
start_label_2 = Label(start_window, text="Enter the password to begin program.", bg='#121212', fg='white', font=('Times New Roman bold', 30), justify="center").grid(row=1, column=0, columnspan=20, ipadx=20, ipady=30, pady=40, sticky="")
password_label = Label(start_window, text="Password", bg='#121212', fg='white', font=('Times New Roman bold', 20), justify="right").grid(row=2, column=0, columnspan=10, ipadx=20, ipady=20, pady=40)
password_entry = Entry(start_window, width=20, font=('Times New Roman bold', 20))
password_entry.grid(row=2, column=1, columnspan=20, ipadx=5, ipady=30, pady=40, padx=(100, 0))
password_entry.config(show="*")

login_btn = Button(start_window, text="Login", bg='#121212', fg='white', font=('Arial bold', 15), command=check_password, width=30, justify=CENTER)
login_btn.grid(row=3, column=0, columnspan=20, ipadx=20, ipady=40, pady=40)





#hello_label = Label(frame_main, text="Hello User!", bg='#121212', fg='white', font=('Times New Roman bold', 60)).grid(row=0, column=0, columnspan=2, ipadx=100, pady=10)
#click_label = Label(frame_main, text="To begin using program, click here: ", bg='#121212', fg='white', font=('Arial bold', 25)).grid(row=2, column=0, pady=10)
#begin_program = Button(frame_main, text="Begin program", bg='#121212', fg='white', font=('Arial bold', 30), command=general, width=30).grid(row=2, column=1, pady=10)


#Commit Changes
conn.commit()

#Close connection
conn.close()

root.mainloop()

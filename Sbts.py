import csv
import os
import pickle
filename="bugs.csv"
pickle_file="bugs.pkl"
bugs=[]
def load_data(pickle_file="bugs.pkl"):
    global bugs
    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as f:
            bugs=pickle.load(f)
        print("Bugs loaded from pickle file.")
    else:
        print(f"file {pickle_file} not found. Starting with empty bug list.")
        bugs=[]
def save_data():    
    with open(pickle_file, "wb") as f:
        pickle.dump(bugs, f)
    with open(filename, "w", newline='') as f:
        fieldnames = [
            "id",
            "title",
            "desc",
            "priority",
            "status",
            "reported_by",
            "assignees",
            "comments",
            "resolution_time",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for b in bugs:
            out = {
                "id": b["id"],
                "title": b["title"],
                "desc": b["desc"],
                "priority": b["priority"],
                "status": b["status"],
                "reported_by": b["reported_by"],
                "assignees":pickle.dumps(list(b.get("assignees", set()))),
                "comments":pickle.dumps(b.get("comments", [])),
                "resolution_time": b.get("resolution_time"),
            }
            writer.writerow(out)
    print("All bugs saved successfully.")
def report_bug(current_user):
    print("---Bug Report----")
    title=input("title:").strip().title()
    desc=input("Description:")
    while True:
        priority=input("Priority(1-5):")
        if priority.isdigit() and 1 <=int(priority)<= 5:
            priority=int(priority)
            break
        print("Invalid Priority")
    bug_id=len(bugs)+1
    bug={
        "id":bug_id,
        "title":title,
        "desc":desc,
        "priority":priority,
        "status":"New",
        "reporter":current_user,
        "assignees":set(),
        "comments":[],
        "reported_by":current_user,
        "resolution_time":None
    }
    bugs.append(bug)
    print(f"Bug {bug_id} reported ! Status:{bug['status']}")
def view_my_bug(current_user):
    print("---My Reported Bugs---")
    found=False
    for b in bugs:
        if b['reported_by']==current_user:
            print(f"ID:{b['id']} Title:{b['title']} Priority:{b['priority']} Status:{b['status']}")
            found=True
    if not found:
        print("No bugs found.")
def add_comment(current_user):
    bug_id=input("Enter bug ID to comment on:")
    if not bug_id.isdigit():
        print("Invalid Bug ID.")
        return
    bug_id = int(bug_id)
    for b in bugs:
        if int(b['id'])==bug_id and b['reported_by']==current_user:
            comment=input("Enter your comment:")
            b['comments'].append(comment)
            print(f"Comment added to bug {bug_id}:{comment}")
            return
def tester_menu(current_user):
    while True:
        print("---Tester Menu---")
        print("1.Report Bug")
        print("2.View My Bugs")
        print("3.Add Comments")
        print("4.Save & Exit")
        choice=input("Choice:")
        if choice=="1":
            report_bug(current_user)
        elif choice=="2":
            view_my_bug(current_user)
        elif choice=="3":
            add_comment(current_user)
        elif choice=="4":
            save_data()
            break
        else:
            print("Invalid Choice")
def claim_bug(current_user):
    bug_id=input("Bug ID:")
    if not bug_id.isdigit():
        print("Invalid Bug ID.")
        return
    bug_id = int(bug_id)
    for b in bugs:
        if int(b['id'])==bug_id and b['status']=='New':
            b['status']='Assigned'
            b['assignees'].add(current_user)
            print(f"Claimed! Status:{b['status']}. Assignees:{b['assignees']}")
            return
    print("Bug not found or already assigned.")
def update_status(current_user):
    bug_id=input("Enter Bug ID to update status:")
    if not bug_id.isdigit():
        print("Invalid Bug ID.")
        return
    bug_id = int(bug_id)
    for b in bugs:
        if int(b['id'])==bug_id:
            new_status=input("Enter new status:").strip().title()
            b['status']=new_status
            print("Updated! Comment added.")
            return
    print("Bug not found.")

def view_assigned_bugs(current_user):
    print("---Assigned Bugs---")
    found=False
    for b in bugs:
        if current_user in b['assignees']:
            print(f"ID:{b['id']} | Title:{b['title']} |  Priority:{b['priority']}  |  Status:{b['status']}")
            found=True
    if not found:
        print("No bugs assigned to you.")
def resolve_bug(current_user):
    bug_id=input("Enter Bug ID to mark resolved:")
    if not bug_id.isdigit():
        print("Invalid Bug ID.")
        return
    bug_id = int(bug_id)
    day=input("Days to Resolve:").strip()
    for b in bugs:
        if int(b['id'])==bug_id and current_user in b['assignees']:
            b['status']='Resolved'
            b['resolution_time']=f"{day} days"
            print(f"Resolution time set:{day} days.")
            return
    print("Bug not found or not assigned to you.")
def save_exit():
    save_data()
    print("Data saved. Exiting Developer Menu.")
def developer_menu(current_user):
    while True:
        print("---Developer Menu---")
        print("1.Claim Bug")
        print("2.Update Status")
        print("3.View Assigned Bugs")
        print("4.Resolve Bug")
        print("5.Save & Exit")
        choice=input("Choice:")
        if choice=="1":
            claim_bug(current_user)
        elif choice=="2":
            update_status(current_user)
        elif choice=="3":
            view_assigned_bugs(current_user)
        elif choice=="4":
            resolve_bug(current_user)
        elif choice=="5":
            save_exit()
            break
        else:
            print("Invalid Choice")
def view_dashboard():
    print("---Dashboard---")
    total_bugs=len(bugs)
    if total_bugs==0:
        print("No bugs found.")
        return
    resolved = 0
    assigned = 0
    new = 0
    # Count each bug by status
    for b in bugs:
        if b["status"] == "Resolved":
            resolved += 1
        elif b["status"] == "Assigned":
            assigned += 1
        elif b["status"] == "New":
            new += 1
    percent_new=(new / total_bugs) * 100
    print(f"Total Bugs: {total_bugs}")
    print(f"open Bugs: {new} ({percent_new:.2f}%)")
    print(f"Assigned: {assigned}")
    print(f"Resolved: {resolved}")
def assign_bug():
    bug_id = input("Enter Bug ID to assign: ")
    if not bug_id.isdigit():
        print("Invalid Bug ID.")
        return
    bug_id = int(bug_id)
    dev = input("Assign to Developer Username: ").strip().lower()
    for b in bugs:
        if b['id'] == bug_id:
            b['assignees'].add(dev)
            b['status'] = "Assigned"
            print(f"Bug #{bug_id} assigned to {dev}.")
            return
    print("Bug not found.")
def generate_report():
    print("\n--- Bug Report ---")
    if not bugs:
        print("No data available.")
        return
    status_count = {}
    for b in bugs:
        s = b['status']
        status_count[s] = status_count.get(s, 0) + 1

    for s, count in status_count.items():
        print(f"{s}: {count}")
    print("Report generated successfully.")
def search_bugs():
    print("Search By:1.Status 2.Priority 3.Assignee")
    choice=int(input("Choice:"))
    if choice==1:
        status=input("Enter Status(New/Assigned/In Progress/Resolved/Closed):").strip().title()
        found=False
        for b in bugs:
            if b['status']==status:
                print(f"ID:{b['id']} Title:{b['title']} Priority:{b['priority']} Status:{b['status']}")
                found=True
        if not found:
            print("No bugs found with this status.")
    elif choice==2:
        priority=input("Enter Priority(1-5):").strip()
        if not priority.isdigit() or not (1 <= int(priority) <= 5):
            print("Invalid Priority.")
            return
        priority = int(priority)
        found=False
        for b in bugs:
            if b['priority']==priority:
                print(f"ID:{b['id']} Title:{b['title']} Priority:{b['priority']} Status:{b['status']}")
                found=True
        if not found:
            print("No bugs found with this priority.")
    elif choice==3:
        assignee=input("Enter Assignee Username:").strip().lower()
        found=False
        for b in bugs:
            if assignee in b['assignees']:
                print(f"ID:{b['id']} Title:{b['title']} Priority:{b['priority']} Status:{b['status']}")
                found=True
        if not found:
            print("No bugs found assigned to this user.")
def manager_menu(current_user):
    while True:
        print("---Manager Menu---")
        print("1.view Dashboard")
        print("2.Assign Bug")
        print("3.Generate Report")
        print("4.Search Bugs")
        print("5.save & Exit")
        choice=input("Choice:")
        if choice=="1":
            view_dashboard()
        elif choice=="2":
            assign_bug()
        elif choice=="3":
            generate_report()
        elif choice=="4":
            search_bugs()
        elif choice=="5":
            save_exit()
            break
        else:
            print("Invalid Choice")
load_data()
while True:
    print("====Software Bug Tracking System (SBTS)===")
    role=input("Enter Role(Tester/Developer/Manager):").title()
    if role=='Tester':
        current_user=input("Login as:(eg. tester1):").strip().lower()
        tester_menu(current_user)
    elif role=="Developer":
        current_user=input("Login as:(eg. dev1):").strip().lower()
        developer_menu(current_user)
    elif role=="Manager":
        current_user=input("Login as:(eg. manager1):").strip().lower()
        manager_menu(current_user)
    else:
        print("Invalid Role")
        break
        

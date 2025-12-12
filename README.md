# Software Bug Tracking System (SBTS)

A console-based Python application to report, track, assign, and resolve software bugs. The system works with three roles: Tester, Developer, and Manager.

## Features

 **Tester**
 - Report Bug
 - View My Bugs
 - Add Comment

 **Developer**

 - Claim Bug
 - Update Status
 - View Assigned Bugs
 - Resolve Bug

 **Manager**
 - View Dashboard
 - Assign Bug
 - Generate CSV Report
 - Search Bugs

## Data Storage

**bugs.csv** → Stores bug details (id, title, desc, priority, status, reported_by).

**users.pkl** → Stores user roles and assigned bugs.

- Extra details like comments/assignees reset on restart.

## How It Works

 - Login with role

 - Choose actions from menu

 - Data saved automatically

 - Reports stored in reports/bug report YYYY-MM-DD.csv

## Submission Phases

**Phase 1:** Tester features

**Phase 2:** Developer features

**Phase 3:** Manager features + full integration

## Installation
Clone this repository:
```bash
git clone https://github.com/komalkumari78/Software-Bug-Tracking-System-Project-.git
cd Software-Bug-Tracking-System-Project

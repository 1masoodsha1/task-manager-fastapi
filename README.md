## Welcome 👋

Thanks for taking the time to work through this exercise!

We don’t expect perfection or a “finished product” in the short time you have. The goal is simply to see how you think,
how you structure code, and how you approach a realistic problem. It’s completely okay if you don’t get through everything.

A few things to keep in mind while you work:

- You’re encouraged to make reasonable assumptions if something isn’t fully specified.
- There isn’t one “right” solution — we’re more interested in your reasoning than in a specific pattern or framework.
- Feel free to leave comments or notes in the code if you’d like to explain trade-offs or what you’d do with more time.

Above all, relax and have fun with it. Treat this as a chance to show how you naturally work on a small but real-world backend feature rather than an exam.

---
## 🚀 Setup Instructions

This project contains two separate applications:

- **Backend** —  FastAPI
- **Frontend** — React (19.2.4) 

You must run **both** for the application to work.

---

## 📦 Setup

### **Requirements**
BE
- Port **57689** must be available

FE
- NPM (or Yarn)
- Port 5173 must be available 

### **Steps**

BE
1. Navigate to the backend directory:

   ```bash
   cd backend
   ```
2. Start the FastAPI application:

   ```bash
   pip install -r requirements.txt
   py run.py
   ```
FE
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   python -m venv .venv
   pip install -r backend/requirements.txt
   ```
3. Start the development server:
   ```
   npm run dev 
   ```
---

## Current API Overview

The backend exposes a simple REST API for managing tasks under the base path:

```text
GET     /api/tasks/             List all tasks
POST    /api/tasks/             Create a new task
GET     /api/tasks/{task_id}/   Get one task by ID
PUT     /api/tasks/{task_id}/   Update a task by ID
DELETE  /api/tasks/{task_id}/   Delete a task by ID
```
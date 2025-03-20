from task_model import Task
from fastapi import FastAPI, Depends

from fastapi.middleware.cors import CORSMiddleware

from db_task_model import create_db_and_tables, get_session
from task_model import Task

from db_task_service import *

from sqlmodel import Session




app = FastAPI()

tasks = [
    Task(),
    Task()
]

# Startup event handler - executes when the application starts
@app.on_event("startup")
def on_startup():
    # Create database tables if they don't exist
    create_db_and_tables()

@app.get("/")
def root():
    return "Hello World"

@app.get("/tasks/all")
def get_all_tasks():
    return tasks

@app.post("/task")
def create_task(task: Task):
    tasks.append(task)
    return "Task Added"

@app.put("/{task_id}")
def update_task(task_id: int, updated: Task):
    for task in tasks:
        if task.id == task_id:
            task.description = updated.description
            task.isComplete = updated.isComplete
            return "Updated task"
    
    return "Task not found"

@app.delete("/task/delete/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return "Deleted task"
    return "Task not found"

@app.get("/get-task/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return "Not found"
        

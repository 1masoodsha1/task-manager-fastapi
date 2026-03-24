from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Response

from ..database import get_connection
from ..schemas import TaskCreate, TaskRead, TaskUpdate


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def validate_due_date_rule(status: str, due_date: Optional[datetime]) -> None:
    if due_date and status != "DONE" and due_date < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail={"dueDate": "Past due date/time is only allowed for completed tasks."},
        )


def row_to_task(row) -> TaskRead:
    return TaskRead(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        status=row["status"],
        dueDate=row["due_date"],
    )


@router.get("/", response_model=list[TaskRead])
def list_tasks() -> list[TaskRead]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, status, due_date FROM tasks ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [row_to_task(row) for row in rows]


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate) -> TaskRead:
    validate_due_date_rule(payload.status, payload.due_date)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, description, status, due_date) VALUES (?, ?, ?, ?)",
        (
            payload.title,
            payload.description,
            payload.status,
            payload.due_date.isoformat() if payload.due_date else None,
        ),
    )
    task_id = cur.lastrowid
    conn.commit()

    cur.execute("SELECT id, title, description, status, due_date FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()
    conn.close()

    return row_to_task(row)


@router.get("/{task_id}/", response_model=TaskRead)
def get_task(task_id: int) -> TaskRead:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, status, due_date FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Not found")

    return row_to_task(row)


@router.put("/{task_id}/", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate) -> TaskRead:
    validate_due_date_rule(payload.status, payload.due_date)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    exists = cur.fetchone()
    if exists is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Not found")

    cur.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, status = ?, due_date = ?
        WHERE id = ?
        """,
        (
            payload.title,
            payload.description,
            payload.status,
            payload.due_date.isoformat() if payload.due_date else None,
            task_id,
        ),
    )
    conn.commit()

    cur.execute("SELECT id, title, description, status, due_date FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()
    conn.close()

    return row_to_task(row)


@router.delete("/{task_id}/", status_code=204)
def delete_task(task_id: int) -> Response:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    exists = cur.fetchone()
    if exists is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Not found")

    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return Response(status_code=204)
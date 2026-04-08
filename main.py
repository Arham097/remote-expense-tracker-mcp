from fastmcp import FastMCP
import os
import tempfile

import aiosqlite

DB_PATH = os.path.join(tempfile.gettempdir(), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    import sqlite3

    with sqlite3.connect(DB_PATH) as c:
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

        c.execute(
            "INSERT OR IGNORE INTO expenses(date, amount, category) VALUES ('2000-01-01', 0, 'test')"
        )
        c.execute("DELETE FROM expenses WHERE category = 'test'")

init_db()

@mcp.tool()
async def add_expense(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database.'''
    async with aiosqlite.connect(DB_PATH) as c:
        cur = await c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        await c.commit()
        return {"status": "ok", "id": cur.lastrowid}


@mcp.tool()
async def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    async with aiosqlite.connect(DB_PATH) as c:
        cur = await c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        rows = await cur.fetchall()
        return [dict(zip(cols, r)) for r in rows]

@mcp.tool()
async def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    async with aiosqlite.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = await c.execute(query, params)
        cols = [d[0] for d in cur.description]
        rows = await cur.fetchall()
        return [dict(zip(cols, r)) for r in rows]

@mcp.tool()
async def update_expense(expense_id, date=None, amount=None, category=None, subcategory=None, note=None):
    '''Update an existing expense entry by ID.'''
    async with aiosqlite.connect(DB_PATH) as c:
        # Build the update query dynamically based on provided fields
        fields = []
        params = []

        if date is not None:
            fields.append("date = ?")
            params.append(date)
        if amount is not None:
            fields.append("amount = ?")
            params.append(amount)
        if category is not None:
            fields.append("category = ?")
            params.append(category)
        if subcategory is not None:
            fields.append("subcategory = ?")
            params.append(subcategory)
        if note is not None:
            fields.append("note = ?")
            params.append(note)

        if not fields:
            return {"status": "error", "message": "No fields to update"}

        params.append(expense_id)
        query = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"
        cur = await c.execute(query, params)
        await c.commit()
        return {"status": "ok", "updated_rows": cur.rowcount}

@mcp.tool()
async def delete_expense(expense_id):
    '''Delete an expense entry by ID.'''
    async with aiosqlite.connect(DB_PATH) as c:
        cur = await c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        await c.commit()
        return {"status": "ok", "deleted_rows": cur.rowcount}

@mcp.tool()
async def add_income(date, amount, category, subcategory="", note=""):
    '''Add a new income entry to the database.'''
    async with aiosqlite.connect(DB_PATH) as c:
        cur = await c.execute(
            "INSERT INTO income(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        await c.commit()
        return {"status": "ok", "id": cur.lastrowid}

@mcp.tool()
async def list_income(start_date, end_date):
    '''List income entries within an inclusive date range.'''
    async with aiosqlite.connect(DB_PATH) as c:
        cur = await c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM income
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        rows = await cur.fetchall()
        return [dict(zip(cols, r)) for r in rows]

@mcp.tool()
async def summarize_income(start_date, end_date, category=None):
    '''Summarize income by category within an inclusive date range.'''
    async with aiosqlite.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM income
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = await c.execute(query, params)
        cols = [d[0] for d in cur.description]
        rows = await cur.fetchall()
        return [dict(zip(cols, r)) for r in rows]

@mcp.tool()
async def update_income(income_id, date=None, amount=None, category=None, subcategory=None, note=None):
    '''Update an existing income entry by ID.'''
    async with aiosqlite.connect(DB_PATH) as c:
        # Build the update query dynamically based on provided fields
        fields = []
        params = []

        if date is not None:
            fields.append("date = ?")
            params.append(date)
        if amount is not None:
            fields.append("amount = ?")
            params.append(amount)
        if category is not None:
            fields.append("category = ?")
            params.append(category)
        if subcategory is not None:
            fields.append("subcategory = ?")
            params.append(subcategory)
        if note is not None:
            fields.append("note = ?")
            params.append(note)

        if not fields:
            return {"status": "error", "message": "No fields to update"}

        params.append(income_id)
        query = f"UPDATE income SET {', '.join(fields)} WHERE id = ?"
        cur = await c.execute(query, params)
        await c.commit()
        return {"status": "ok", "updated_rows": cur.rowcount}

@mcp.tool()
async def delete_income(income_id):
    '''Delete an income entry by ID.'''
    async with aiosqlite.connect(DB_PATH) as c:
        cur = await c.execute("DELETE FROM income WHERE id = ?", (income_id,))
        await c.commit()
        return {"status": "ok", "deleted_rows": cur.rowcount}

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

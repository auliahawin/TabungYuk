import sqlite3
from pathlib import Path
import hashlib


class Database:

    def __init__(self):
        self.db_path = Path(__file__).resolve().parent / "tabungyuk.db"
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        c = self.connection.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                profile_photo TEXT DEFAULT ''
            )
        """)

        # Untuk database lama yang belum punya profile_photo
        try:
            c.execute(
                "ALTER TABLE users ADD COLUMN profile_photo TEXT DEFAULT ''"
            )
        except sqlite3.OperationalError:
            pass

        c.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                target INTEGER NOT NULL,
                image TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS tabungan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER NOT NULL,
                jumlah INTEGER NOT NULL,
                keterangan TEXT NOT NULL,
                tanggal TEXT NOT NULL,
                FOREIGN KEY(goal_id) REFERENCES goals(id)
                    ON DELETE CASCADE
            )
        """)

        self.connection.commit()

    def register(self, username, password):
        try:
            password_hash = hashlib.sha256(
                password.encode()
            ).hexdigest()

            self.connection.execute(
                """
                INSERT INTO users
                (username, password, profile_photo)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, "")
            )

            self.connection.commit()
            return True

        except sqlite3.IntegrityError:
            return False

    def login(self, username, password):
        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        return self.connection.execute(
            """
            SELECT id, username, profile_photo
            FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password_hash)
        ).fetchone()

    def update_profile_photo(self, user_id, photo):
        self.connection.execute(
            """
            UPDATE users
            SET profile_photo = ?
            WHERE id = ?
            """,
            (photo, user_id)
        )
        self.connection.commit()

    def add_goal(self, user_id, name, target, image):
        self.connection.execute(
            """
            INSERT INTO goals
            (user_id, name, target, image, created_at)
            VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
            """,
            (user_id, name, target, image)
        )
        self.connection.commit()

    def get_goals(self, user_id):
        return self.connection.execute(
            """
            SELECT id, name, target, image, created_at
            FROM goals
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    def get_goal(self, goal_id):
        return self.connection.execute(
            """
            SELECT id, user_id, name, target, image, created_at
            FROM goals
            WHERE id = ?
            """,
            (goal_id,)
        ).fetchone()

    def get_goal_total(self, goal_id):
        row = self.connection.execute(
            """
            SELECT COALESCE(SUM(jumlah), 0) AS total
            FROM tabungan
            WHERE goal_id = ?
            """,
            (goal_id,)
        ).fetchone()

        return row["total"]

    def add_saving(
        self,
        goal_id,
        jumlah,
        keterangan,
        tanggal
    ):
        self.connection.execute(
            """
            INSERT INTO tabungan
            (goal_id, jumlah, keterangan, tanggal)
            VALUES (?, ?, ?, ?)
            """,
            (goal_id, jumlah, keterangan, tanggal)
        )

        self.connection.commit()

    def get_goal_savings(self, goal_id):
        return self.connection.execute(
            """
            SELECT id, jumlah, keterangan, tanggal
            FROM tabungan
            WHERE goal_id = ?
            ORDER BY id DESC
            """,
            (goal_id,)
        ).fetchall()

    def delete_goal(self, goal_id):
        self.connection.execute(
            "DELETE FROM tabungan WHERE goal_id = ?",
            (goal_id,)
        )

        self.connection.execute(
            "DELETE FROM goals WHERE id = ?",
            (goal_id,)
        )

        self.connection.commit()

    def close(self):
        self.connection.close()
import sqlite3

class DataNexus:
    def __init__(self, db_path='nexus_data.db'):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS repositories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    format TEXT NOT NULL
                )
                CREATE TABLE IF NOT EXISTS components (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    format TEXT,
                    group TEXT,
                    version TEXT,
                    repository_id INTEGER NOT NULL,
                    FOREIGN KEY (repository_id) REFERENCES repositories(id)
                )
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    asset_id TEXT NOT NULL,
                    file_size INTEGER,
                    last_modified TEXT,
                    last_downloaded TEXT,
                    uploaded_by TEXT,
                    blob_created TEXT,
                    blob_store_name TEXT,
                    format TEXT,
                    path TEXT,
                    download_url TEXT,
                    content_type TEXT,
                    repository_id INTEGER NOT NULL,
                    FOREIGN KEY (repository_id) REFERENCES repositories(id)
                )
            ''')

    def save_repository(self, name, format):
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO repositories (name, format) VALUES (?, ?)
            ''', (name, format))
            return cursor.lastrowid

    def save_asset(self, name, asset_id, file_size, last_modified, last_downloaded, uploaded_by, blob_created, blob_store_name, format, path, download_url, content_type, repository_id):
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO assets (name, asset_id, file_size, last_modified, last_downloaded, uploaded_by, blob_created, blob_store_name, format, path, download_url, content_type, repository_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, asset_id, file_size, last_modified, last_downloaded, uploaded_by, blob_created, blob_store_name, format, path, download_url, content_type, repository_id))
            return cursor.lastrowid

    def save_component(self, name, format, group, version, repository_id):
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO components (name, format, group, version, repository_id) VALUES (?, ?, ?, ?, ?)
            ''', (name, format, group, version, repository_id))
            return cursor.lastrowid

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None


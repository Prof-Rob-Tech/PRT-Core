"""
===========================================================
PRT Labs - Database / DB Manager
Class: DatabaseManager

Description:
    Gerenciador do Banco de Dados SQLite local (nexus.db).
    Armazena histórico, downloads concluídos e favoritos.
===========================================================
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional


class DatabaseManager:
    """Gerenciador central SQLite para armazenamento local do PRT Nexus."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path: Optional[str] = None) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        if db_path:
            self.db_path = db_path
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_dir = os.path.join(base_dir, "database")
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, "nexus.db")

        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Cria uma nova conexão segura por chamada/thread."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Cria as tabelas caso não existam."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Tabela de Downloads / Biblioteca
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    platform TEXT,
                    file_path TEXT,
                    file_size TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Tabela de Favoritos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    platform TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 3. Tabela de Histórico
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    platform TEXT,
                    action_type TEXT DEFAULT 'download',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()

    # ==========================================
    # 📥 MÉTODOS DE DOWNLOADS / BIBLIOTECA
    # ==========================================

    def add_download(self, task_id: str, title: str, url: str, platform: str, file_path: str = "", file_size: str = "", status: str = "Concluído") -> int:
        """Registra um download na biblioteca."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO downloads (task_id, title, url, platform, file_path, file_size, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (task_id, title, url, platform, file_path, file_size, status))
            conn.commit()
            return cursor.lastrowid

    def get_all_downloads(self) -> List[Dict[str, Any]]:
        """Retorna todos os downloads cadastrados."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM downloads ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    # ==========================================
    # ⭐ MÉTODOS DE FAVORITOS
    # ==========================================

    def add_favorite(self, title: str, url: str, platform: str = "geral") -> int:
        """Adiciona um item aos favoritos."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO favorites (title, url, platform)
                VALUES (?, ?, ?)
            """, (title, url, platform))
            conn.commit()
            return cursor.lastrowid

    def get_all_favorites(self) -> List[Dict[str, Any]]:
        """Retorna todos os favoritos."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM favorites ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def remove_favorite(self, fav_id: int) -> None:
        """Remove um item dos favoritos pelo ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
            conn.commit()

    # ==========================================
    # 🕒 MÉTODOS DE HISTÓRICO
    # ==========================================

    def add_history(self, title: str, url: str, platform: str = "geral", action_type: str = "download") -> int:
        """Adiciona uma entrada ao histórico de navegação/extração."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO history (title, url, platform, action_type)
                VALUES (?, ?, ?, ?)
            """, (title, url, platform, action_type))
            conn.commit()
            return cursor.lastrowid

    def get_all_history(self) -> List[Dict[str, Any]]:
        """Retorna todo o histórico de atividades."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def clear_history(self) -> None:
        """Limpa todo o histórico de atividades."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history")
            conn.commit()


# Instância global Singleton
db_manager = DatabaseManager()
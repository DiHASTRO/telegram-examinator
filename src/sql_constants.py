TABLES_INIT_QUERIES = {
    'users':                    """
                                CREATE TABLE users (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        tg_user_id INTEGER NOT NULL UNIQUE,
                                        state INTEGER NOT NULL DEFAULT 0,
                                        additional_info INTEGER
                                );""",
    'subjects':                 """
                                CREATE TABLE subjects (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    owner_user_id INTEGER NOT NULL,
                                    FOREIGN KEY (owner_user_id) REFERENCES users (id) ON DELETE CASCADE
                                );""",
    'attempts':                 """
                                CREATE TABLE attempts (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    date INTEGER NOT NULL,
                                    user_id INTEGER NOT NULL,
                                    subject_id INTEGER NOT NULL,
                                    grade INTEGER NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                                    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
                                );""",
    'users_subjects_mtm':       """
                                CREATE TABLE user_subjects_mtm (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER NOT NULL,
                                    subject_id INTEGER NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                                    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
                                );""",
    'questions':                """
                                CREATE TABLE questions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    subject_id INTEGER NOT NULL,
                                    answer_id INTEGER NOT NULL UNIQUE,
                                    question_text TEXT,
                                    photo1 TEXT,
                                    photo2 TEXT,
                                    photo3 TEXT,
                                    photo4 TEXT,
                                    photo5 TEXT,
                                    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
                                    FOREIGN KEY (answer_id) REFERENCES answers (id) ON DELETE CASCADE
                                );""",
    'answers':                  """
                                CREATE TABLE answers (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    question_id INTEGER NOT NULL UNIQUE,
                                    answer_text TEXT,
                                    photo1 TEXT,
                                    photo2 TEXT,
                                    photo3 TEXT,
                                    photo4 TEXT,
                                    photo5 TEXT,
                                    FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
                                );"""
}

PRAGMA_QUERIES = {
    'turn_foreign_keys_on': 'PRAGMA foreign_keys = ON;',
}

INSERT_QUERIES = {
    'common_insert': 'INSERT INTO {0} {1} VALUES {2};',
}

SELECT_QUERIES = {
    'get_by_column': 'SELECT * FROM {0} WHERE {1} = {2}',
}

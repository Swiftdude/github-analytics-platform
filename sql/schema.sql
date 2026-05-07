CREATE TABLE repositories (
    id INTEGER PRIMARY KEY,
    owner TEXT NOT NULL,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL UNIQUE,
    primary_language TEXT,
    stars INTEGER NOT NULL DEFAULT 0,
    forks INTEGER NOT NULL DEFAULT 0,
    watchers INTEGER NOT NULL DEFAULT 0,
    open_issues INTEGER NOT NULL DEFAULT 0,
    collected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE repository_languages (
    repository_id INTEGER NOT NULL,
    language TEXT NOT NULL,
    bytes_of_code INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (repository_id, language),
    FOREIGN KEY (repository_id) REFERENCES repositories (id)
);

CREATE TABLE commits (
    sha TEXT PRIMARY KEY,
    repository_id INTEGER NOT NULL,
    author TEXT NOT NULL,
    authored_at TIMESTAMP NOT NULL,
    additions INTEGER NOT NULL DEFAULT 0,
    deletions INTEGER NOT NULL DEFAULT 0,
    changed_files INTEGER NOT NULL DEFAULT 0,
    message TEXT,
    FOREIGN KEY (repository_id) REFERENCES repositories (id)
);

CREATE TABLE issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repository_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,
    FOREIGN KEY (repository_id) REFERENCES repositories (id)
);

CREATE TABLE analytics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repository_id INTEGER NOT NULL,
    bus_factor REAL NOT NULL,
    commit_entropy REAL NOT NULL,
    commit_frequency_per_day REAL NOT NULL,
    avg_commit_churn REAL NOT NULL,
    churn_volatility REAL NOT NULL,
    avg_issue_resolution_hours REAL NOT NULL,
    maintainability_score REAL NOT NULL,
    inactivity_risk REAL NOT NULL,
    predicted_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (repository_id) REFERENCES repositories (id)
);

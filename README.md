# GitHub Analytics Platform

This project is a starter implementation of a resume-level GitHub analytics system that can ingest repository data, compute engineering health metrics, estimate maintainability risk, and generate practical recommendations.

## What It Does

- Pulls repository metadata, languages, commits, and issues from the GitHub API
- Computes metrics such as bus factor, commit entropy, churn, contributor spread, and issue resolution speed
- Runs a lightweight ML-backed repository health model
- Produces recommendation text explaining why a repository may be healthy, fragile, or at risk
- Falls back to sample data so the project still runs without a GitHub token

## Project Structure

```text
github_analytics_platform/
  github_client.py      GitHub ingestion layer
  metrics.py            Analytics and derived repository metrics
  ml.py                 Repository health scoring model
  recommendations.py    Human-readable recommendation engine
  sample_data.py        Local demo snapshot for offline runs
  models.py             Shared domain models
  main.py               Analysis orchestration
sql/schema.sql          Starter relational schema for storing snapshots
run_analysis.py         CLI entrypoint
```

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add a GitHub token to `.env` if you want live API data:

```env
GITHUB_TOKEN=your_token_here
```

4. Run with sample data:

```bash
python run_analysis.py
```

5. Run against a real repository:

```bash
python run_analysis.py --owner openai --repo openai-python --format json
```

## Current Metrics

- `bus_factor`: How many contributors account for at least half the commits
- `commit_entropy`: How evenly commit volume is distributed across contributors
- `avg_commit_churn`: Mean additions plus deletions per commit
- `churn_volatility`: Variability in change size across commits
- `commit_frequency_per_day`: Recent commit density over the sampled time window
- `avg_issue_resolution_hours`: Mean issue close time for closed issues
- `high_churn_files`: Most frequently touched files in the sampled commits

## Good Next Steps

- Add persistent SQL storage for repository snapshots and time-series analytics
- Expose this package through a FastAPI backend for a React dashboard
- Train the model on a real labeled dataset instead of bootstrap seed data
- Add contributor impact charts, inactivity forecasts, and repo-to-repo comparisons
- Integrate linting, test coverage, and pull request review signals

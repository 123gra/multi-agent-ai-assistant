# multi-agent-ai-assistant

## Overview
This project implements a multi-agent AI system that manages tasks, schedules, and notes.

## Features
- Main agent coordinating sub-agents
- Task, Calendar, Notes agents
- SQLite database storage
- API-based system using FastAPI

## API
POST /execute

Example:
{
  "query": "Schedule a meeting and add a task"
}

## Tech Stack
- FastAPI
- SQLite
- Python

## Deployment
Deployed using Google Cloud Run- https://multi-agent-ai-assistant.onrender.com/

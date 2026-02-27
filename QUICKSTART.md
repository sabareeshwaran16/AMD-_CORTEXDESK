# Quick Start Guide

## Installation (5 minutes)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the system:**
   ```bash
   python test_system.py
   ```

## Usage

### Web Interface (Recommended)

1. **Start the server:**
   ```bash
   python src/api.py
   ```

2. **Open the UI:**
   - Open `src/ui/index.html` in your browser
   - Or visit `http://127.0.0.1:8000/docs` for API docs

3. **Upload a document:**
   - Click the upload zone
   - Select a PDF, DOCX, XLSX, or TXT file
   - Wait for processing (2-5 seconds)

4. **View extracted tasks:**
   - Tasks appear automatically in the Tasks panel
   - Color-coded by priority (red=urgent, orange=high)

### Command Line Interface

```bash
python src/cli.py
```

Follow the menu prompts.

### Python API

```python
from src.core.workspace_assistant import WorkspaceAssistant

# Start
assistant = WorkspaceAssistant()
assistant.start()

# Process file
assistant.process_file("meeting_notes.txt")

# Get tasks
tasks = assistant.get_tasks()
print(tasks)

# Stop
assistant.stop()
```

## Example Use Cases

### 1. Extract Action Items from Meeting Notes

Create `meeting.txt`:
```
Meeting: Q1 Planning
John will review budget by Friday
Sarah needs to prepare slides
TODO: Mike schedule follow-up
```

Process:
```python
assistant.process_file("meeting.txt")
tasks = assistant.get_tasks()
# Returns: [{"task": "review budget", "assignee": "John", ...}, ...]
```

### 2. Search Documents

```python
assistant.process_file("project_docs.pdf")
assistant.search("deadline")
```

### 3. Track Decisions

Meeting notes with "Decided:" or "Agreed:" are automatically tracked in episodic memory.

## Tips

- **Supported formats:** PDF, DOCX, XLSX, TXT
- **Task detection:** Use keywords like "TODO", "Action", "@name"
- **Deadlines:** Include dates in format YYYY-MM-DD or "by Friday"
- **Priority:** Use words like "urgent", "critical", "important"

## Troubleshooting

**Problem:** Import errors
```bash
pip install -r requirements.txt --upgrade
```

**Problem:** No tasks extracted
- Check file format is supported
- Ensure text contains action keywords
- View agent status in UI

**Problem:** Slow processing
- Reduce file size
- Process one file at a time
- Check system resources

## Next Steps

1. Upload your first document
2. Review extracted tasks
3. Customize agent behavior in `config/config.json`
4. Add more agents (see README.md)

## Support

- Check README.md for detailed documentation
- Review code comments for implementation details
- All processing is local - no internet required

# Markdown Projects Page Guide

## Overview

The projects page uses server-side Python to render markdown content into HTML. This allows you to easily update the projects page by editing a simple markdown file instead of manually writing HTML.

## How It Works

1. **Source File**: Edit `backend/content/projects.md` with your project content in markdown format
2. **Build Script**: Run `python3 backend/build_projects.py` to convert markdown to HTML
3. **Output**: The script generates `frontend/public/projects.html` with full page styling

## Updating Projects

### 1. Edit the Markdown File

Open `backend/content/projects.md` and update your projects using this format:

```markdown
# Featured Projects

## Project Name
**Year** | Project Type | Technologies

- Bullet point describing achievement
- Another bullet point
- And more details

## Another Project
**2024** | Web Application | Python, AWS

- Key accomplishment
- Another achievement
```

### 2. Build the HTML

Run the build script from the project root:

```bash
python3 backend/build_projects.py
```

You should see:
```
Reading /path/to/backend/content/projects.md...
Converting markdown to HTML...
Generating full HTML page...
Writing to /path/to/frontend/public/projects.html...
Build complete!
```

### 3. Preview Locally

Open `frontend/public/projects.html` in your browser to preview the changes.

### 4. Deploy

Commit and push your changes:

```bash
git add backend/content/projects.md frontend/public/projects.html
git commit -m "Update projects page"
git push
```

## Markdown Syntax Supported

The build script uses Python's `markdown` library with the following features:

- **Headers**: Use `#` for h1, `##` for h2, etc.
- **Bold**: Use `**text**` for bold text
- **Lists**: Use `-` or `*` for bullet points
- **Links**: Use `[text](url)` for links
- **Line breaks**: Automatic line break support with `nl2br` extension
- **Tables**: Supported via `extra` extension

## File Structure

```
cloud-resume-challenge/
├── backend/                   # Backend scripts and content
│   ├── build_projects.py     # Build script
│   ├── requirements.txt      # Python dependencies
│   └── content/
│       └── projects.md       # Markdown source (EDIT THIS)
└── frontend/                  # Frontend static files
    └── public/
        ├── projects.html     # Generated HTML (DO NOT EDIT)
        └── assets/
            └── styles.css    # Includes markdown styling
```

## Dependencies

The build script requires Python 3 and the `markdown` library:

```bash
pip install -r backend/requirements.txt
```

## Styling

The markdown content is wrapped in a `<div class="markdown-content">` element with custom CSS styling in `frontend/public/assets/styles.css`. The styles are responsive and match the rest of the site.

## Benefits

- **Easy Updates**: Edit plain text markdown instead of HTML
- **Version Control**: Track changes to content easily
- **Consistency**: Automatic styling ensures visual consistency
- **No Client-Side JS**: All rendering happens server-side (build-time)
- **Static Deployment**: Output is still a static HTML file

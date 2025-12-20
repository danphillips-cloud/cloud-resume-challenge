# Backend

This directory contains the backend scripts and content for server-side rendering of the website.

## Directory Structure

```
backend/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── build_projects.py      # Build script for projects page
└── content/              # Markdown content files
    └── projects.md       # Projects page content
```

## Purpose

The backend handles server-side (build-time) conversion of markdown content to HTML, allowing for easy content updates without directly editing HTML files.

## Usage

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### Build Projects Page

From the project root directory:

```bash
python3 backend/build_projects.py
```

This will:
1. Read `backend/content/projects.md`
2. Convert markdown to HTML
3. Generate `frontend/public/projects.html` with full page template

## Adding New Content Pages

To add additional markdown-rendered pages:

1. Create a new markdown file in `backend/content/`
2. Create a corresponding build script (or extend the existing one)
3. Add necessary CSS styling in `frontend/public/assets/styles.css`
4. Run the build script to generate the HTML

## Dependencies

- **Python 3**: Required to run build scripts
- **markdown**: Python library for markdown parsing and HTML conversion
  - Extensions enabled: `extra`, `nl2br`

## Development Workflow

1. Edit markdown content in `backend/content/`
2. Run build script: `python3 backend/build_projects.py`
3. Preview changes locally
4. Commit and deploy

## Notes

- All rendering is done at build-time (server-side), not client-side
- Generated HTML files are static and can be deployed to any static hosting service
- The build script uses absolute paths, so it can be run from anywhere

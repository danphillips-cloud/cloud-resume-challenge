# Backend

This directory contains the backend scripts and content for server-side rendering of the website.

## Overview

The projects page uses server-side Python to render markdown content into HTML. This allows you to easily update the projects page by editing a simple markdown file instead of manually writing HTML.

## Directory Structure

```
backend/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── build_projects.py      # Build script for projects page
└── content/
    └── projects/         # Individual project markdown files (EDIT THESE)
        ├── cloud-resume-challenge.md
        ├── enterprise-data-migration.md
        ├── infrastructure-automation.md
        └── multi-environment-ecs.md
```

## Quick Start

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
1. Read all markdown files from `backend/content/projects/`
2. Combine them into a single page
3. Convert markdown to HTML
4. Generate `frontend/public/projects.html` with full page template

## Updating Projects

### 1. Edit or Add Project Files

Each project has its own markdown file in `backend/content/projects/`. To add or edit a project:

**To edit an existing project:**
Open the corresponding `.md` file and update the content.

**To add a new project:**
Create a new `.md` file in `backend/content/projects/` using this format:

```markdown
## Project Name
**Year** | Project Type | Technologies

- Bullet point describing achievement
- Another bullet point
- And more details
```

Example filename: `my-new-project.md`

**To remove a project:**
Simply delete the corresponding `.md` file.

### 2. Build the HTML

Run the build script from the project root:

```bash
python3 backend/build_projects.py
```

You should see:
```
Reading project files from /path/to/backend/content/projects...
  Reading cloud-resume-challenge.md...
  Reading enterprise-data-migration.md...
  Reading infrastructure-automation.md...
  Reading multi-environment-ecs.md...
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
git add backend/content/projects/ frontend/public/projects.html
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

## Project Structure

```
cloud-resume-challenge/
├── backend/                   # Backend scripts and content
│   ├── build_projects.py     # Build script
│   ├── requirements.txt      # Python dependencies
│   └── content/
│       └── projects/         # Individual project files (EDIT THESE)
│           ├── cloud-resume-challenge.md
│           ├── enterprise-data-migration.md
│           ├── infrastructure-automation.md
│           └── multi-environment-ecs.md
└── frontend/                  # Frontend static files
    └── public/
        ├── projects.html     # Generated HTML (DO NOT EDIT)
        └── assets/
            └── styles.css    # Includes markdown styling
```

## Dependencies

- **Python 3**: Required to run build scripts
- **markdown**: Python library for markdown parsing and HTML conversion
  - Extensions enabled: `extra`, `nl2br`

## Styling

The markdown content is wrapped in a `<div class="markdown-content">` element with custom CSS styling in `frontend/public/assets/styles.css`. The styles are responsive and match the rest of the site.

## Benefits

- **Easy Updates**: Edit plain text markdown instead of HTML
- **Version Control**: Track changes to content easily
- **Consistency**: Automatic styling ensures visual consistency
- **No Client-Side JS**: All rendering happens server-side (build-time)
- **Static Deployment**: Output is still a static HTML file

## Managing Projects

### Adding a New Project

1. Create a new `.md` file in `backend/content/projects/`
2. Follow the markdown format (see example above)
3. Run the build script: `python3 backend/build_projects.py`
4. Commit and deploy

### Project Display Order

Projects are displayed in alphabetical order by filename. To control the order, you can prefix filenames with numbers:
- `01-cloud-resume-challenge.md`
- `02-multi-environment-ecs.md`
- etc.

## Adding New Content Pages

To add additional markdown-rendered pages (beyond projects):

1. Create a new directory in `backend/content/`
2. Create a corresponding build script (or extend the existing one)
3. Add necessary CSS styling in `frontend/public/assets/styles.css`
4. Run the build script to generate the HTML

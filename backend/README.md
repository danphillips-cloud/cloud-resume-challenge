# Backend -WIP

This directory contains the backend scripts and content for server-side rendering of the website.

## Overview

The backend contains:

1. **Build Scripts**: Server-side Python scripts to render markdown content into HTML
2. **Mock Counter API**: A simple Flask API for testing the visitor counter functionality

The projects page uses server-side Python to render markdown content into HTML. This allows you to easily update the projects page by editing a simple markdown file instead of manually writing HTML.

## Design Decisions

### Why Markdown Over Direct HTML Editing?

Markdown provides a clean, version-control-friendly way to manage content without dealing with HTML tags, CSS classes, or layout concerns. Writing project descriptions becomes as simple as editing a text file—no risk of breaking tags, forgetting closing divs, or introducing inconsistent styling.

### Why Server-Side Rendering?

Build-time rendering (server-side) means:

- **Static Output**: The final HTML is a static file, perfect for S3/CloudFront deployment
- **No Client-Side Dependencies**: No JavaScript frameworks or markdown parsers needed in the browser
- **Fast Load Times**: Pre-rendered HTML loads instantly—no runtime compilation
- **SEO Friendly**: Search engines see the full rendered content immediately
- **Simple Deployment**: Just upload the generated HTML file

### Why Python?

Python's `markdown` library is mature, well-documented, and handles edge cases gracefully. Since this is a build-time tool (not runtime), there's no performance concern—and Python's simplicity makes the build script easy to understand and modify.

### Benefits of This Approach

- **Separation of Concerns**: Content (markdown) lives separately from presentation (HTML/CSS)
- **Easy Updates**: Non-technical updates don't require touching HTML
- **Version Control**: Git diffs on markdown files are human-readable
- **Consistency**: Automated rendering ensures uniform styling across all projects
- **Maintainability**: Single build script handles all content transformation

## Directory Structure

```text
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

```text
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

```text
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

---

## Mock Counter API

A simple Flask API for testing the visitor counter functionality during development.

### Features

- **In-Memory Counter**: Maintains a counter that increments with each request
- **CORS Enabled**: Supports cross-origin requests from the frontend
- **Simple REST API**: POST to increment, GET to retrieve current count
- **Health Check**: Endpoint to verify API is running

### Getting Started

1. **Install Dependencies**

```bash
pip install -r backend/requirements.txt
```

1. **Run the API**

```bash
python3 backend/mock_counter_api.py
```

The API will start on `http://localhost:5000`

### API Endpoints

#### POST /api/visitor-count

Increment and return the visitor count.

**Response:**

```json
{
  "count": 42,
  "message": "Counter incremented successfully"
}
```

#### GET /api/visitor-count

Get the current count without incrementing.

**Response:**

```json
{
  "count": 42,
  "message": "Current count retrieved"
}
```

#### GET /api/health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "message": "Mock Counter API is running"
}
```

### Testing with Frontend

To use the mock API with your frontend:

1. Start the mock API server (see Quick Start above)
2. Update the frontend configuration in `frontend/public/assets/visitor-counter.js`:

   ```javascript
   const config = {
      awsEndpoint: 'http://localhost:5000/api/visitor-count',
      activeBackend: 'aws'
   };
   ```

3. Open your frontend in a browser and the counter should work!

### Configuration

The API can be configured via environment variables:

- `PORT`: Server port (default: 5000)
- `DEBUG`: Enable debug mode (default: True)

Example:

```bash
PORT=8080 DEBUG=False python3 backend/mock_counter_api.py
```

### Notes

- The counter is stored in memory and resets when the server restarts
- This is for development/testing only - use a real database for production
- CORS is enabled for all origins to simplify local development

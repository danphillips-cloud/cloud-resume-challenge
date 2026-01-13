# Backend

Build scripts and a rudimentary "content management system" for server-side rendering and local development.

## Overview

The backend is a lightweight Python-based build system that handles server-side rendering of Markdown content into static HTML. It includes development tools for testing the visitor counter without touching AWS/GCP resources.

## Features

- **Server-Side Rendering**: Build-time Markdown to HTML conversion with Python
- **Content Management**: Simple Markdown files for managing project descriptions
- **Mock Counter API**: Flask-based local API for testing visitor counter integration
- **Static Output**: Generates deployment-ready static HTML files
- **No Client Dependencies**: Pre-rendered content loads instantly without runtime compilation
- **Version Control Friendly**: Human-readable Markdown diffs for content changes

## Quick Start

For frontend setup (static files, HTML resume), see [`frontend/README.md`](../frontend/README.md).

### Install Dependencies

Create your requirements.txt file
```
markdown==3.5.1
flask==3.0.0
flask-cors==4.0.0
```

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

## Directory Structure

```text
backend/
├── README.md                    # This file
├── requirements.txt             # Python dependencies (build scripts)
├── build_projects.py            # Build script for projects page
├── build_blog.py                # Build script for blog page
├── mock_counter_api.py          # Local API mock for testing
├── lambda/                      # Lambda function code
│   ├── app.py                   # Visitor counter Lambda handler
│   └── requirements.txt         # Lambda runtime dependencies
└── content/
    ├── projects/                # Individual project markdown files (EDIT THESE)
    └── blog/                    # Individual blog post markdown files (EDIT THESE)
```

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
Repeat the same steps for blog (more below).

## Markdown Syntax Supported

The build script uses Python's `markdown` library with the following features:

- **Headers**: Use `#` for h1, `##` for h2, etc.
- **Bold**: Use `**text**` for bold text
- **Lists**: Use `-` or `*` for bullet points
- **Links**: Use `[text](url)` for links
- **Line breaks**: Automatic line break support with `nl2br` extension
- **Tables**: Supported via `extra` extension

## Configuration

### Content Display Order

Both blog posts and projects are displayed in alphabetical order by filename. To control the display order, prefix filenames with numbers:

**Blog posts** (currently using numbered prefixes):
```text
backend/content/blog/
├── 01-welcome-to-my-blog.md
├── 02-infrastructure-as-code-best-practices.md
└── 03-ecs-vs-eks.md
```

**Projects** (currently alphabetical):
```text
backend/content/projects/
├── cloud-resume-challenge.md
├── enterprise-data-migration.md
├── infrastructure-automation.md
└── multi-environment-ecs.md
```

**Note:** The numbered prefix approach is a pragmatic temporary solution and is something I plan to explore as the blog grows and ordering becomes more complex. Maybe a good time to try [Hugo](https://gohugo.io/).

---

## Development Journey

This section documents the development process and design decisions made while building the backend. I'm sure I'll have to make adjustments as the project evolves, but this is how it all started.

### Content Management Approach

After completing the static HTML resume for the frontend, I needed a way to manage project descriptions without manually editing HTML. I wanted something simple that would let me focus on content rather than markup.

### Choosing Markdown and Server-Side Rendering

I decided on a Markdown-based approach with build-time rendering:

**Why Markdown?**
- Clean, version-control-friendly content management
- No HTML tags or CSS classes to worry about
- Familiar syntax from documentation work
- Human-readable diffs in Git

I chose Python for the build script because the `markdown` library is mature and well-documented. The script is under 50 lines of code and easy to modify.

### Build Script Implementation

The `build_projects.py` and `build_blog.py` scripts:
1. Reads all `.md` files from `backend/content/projects/`or `backend/content/blog/`
2. Combines them into a single content block
3. Converts Markdown to HTML using Python's markdown library
4. Generates the full `projects.html` or `blog.html` page with navigation and styling
5. Outputs to `frontend/public/` for deployment

This keeps content separate from presentation. I can update projects by editing plain text files, and the build script ensures consistent styling. Not ideal in the long run, but for starting off it's fine. 

### Mock Counter API Development

For local development of the visitor counter feature, I'm using a simple Flask-based mock API. This avoids hitting AWS/GCP endpoints during development—no authentication setup, no costs, faster iteration.

The mock API provides the same endpoints as the production API but stores the counter in memory.

---

## Mock Counter API

A simple Flask API for testing the visitor counter functionality during local development without touching AWS/GCP resources.

### Quick Start

Install dependencies and run the API:

```bash
pip install -r backend/requirements.txt
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

To use the mock API with the frontend visitor counter:

1. Start the mock API server (see Quick Start above)
2. Update `frontend/public/assets/visitor-counter.js`:

```javascript
const config = {
   awsEndpoint: 'http://localhost:5000/api/visitor-count',
  };
```

3. Open your frontend in a browser—the counter should work locally

For more details on frontend configuration, see [`frontend/README.md`](../frontend/README.md#visitor-counter).

### Configuration

Configure via environment variables:

```bash
PORT=8080 DEBUG=False python3 backend/mock_counter_api.py
```

- `PORT`: Server port (default: 5000)
- `DEBUG`: Enable debug mode (default: True)

### Notes

- Counter resets when server restarts (in-memory storage)
- For development/testing only—use AWS/GCP for production
- CORS enabled for all origins to simplify local development

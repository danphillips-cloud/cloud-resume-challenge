#!/usr/bin/env python3
"""
Build script to convert blog markdown files to blog.html
This script reads individual blog post markdown files and generates a complete HTML page
"""

import markdown
import os
import glob


def read_markdown_file(filepath):
    """Read the markdown file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def read_all_posts(blog_dir):
    """Read all markdown files from the blog directory and combine them"""
    # Get all .md files in the blog directory
    post_files = sorted(glob.glob(os.path.join(blog_dir, '*.md')))

    if not post_files:
        print(f"Warning: No blog post files found in {blog_dir}")
        return ""

    # Start with the header
    combined_content = "# Blog Posts\n\n"

    # Read and combine all blog post files
    for post_file in post_files:
        print(f"  Reading {os.path.basename(post_file)}...")
        content = read_markdown_file(post_file)
        combined_content += content + "\n\n"

    return combined_content


def convert_markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    return md.convert(md_content)


def create_html_page(content_html):
    """Wrap the markdown-generated HTML in the full page template"""
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dan Phillips - Blog</title>
    <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <nav class="nav-bar">
        <div class="nav-left">
            <a href="index.html">Home</a>
            <a href="blog.html" class="active">Blog</a>
            <a href="resume.html">Resume</a>
            <a href="projects.html">Projects</a>
            <a href="certifications.html">Certifications</a>
        </div>
        <div class="nav-right">
            <a href="https://linkedin.com/in/danphillips-cloud" target="_blank" aria-label="LinkedIn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
            </a>
            <a href="https://github.com/danphillips-cloud" target="_blank" aria-label="GitHub">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
            </a>
        </div>
    </nav>

    <div id="main-content" class="profile-header">
        <div class="profile-image-container">
            <img src="assets/images/Profile_2024.jpg" alt="Professional headshot of Dan Phillips" class="profile-image">
        </div>
        <div class="profile-info">
            <h1>Blog</h1>
            <p style="color: #666; font-size: 16px; margin-top: 10px;">More posts coming soon - here's a preview of what's to come</p>
        </div>
    </div>

    <div class="markdown-content">
        {content_html}
    </div>

</body>
</html>
"""
    return template


def main():
    """Main build function"""
    # Get the script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Define paths relative to project root
    blog_dir = os.path.join(script_dir, 'content', 'blog')
    html_file = os.path.join(project_root, 'frontend', 'public', 'blog.html')

    # Check if blog directory exists
    if not os.path.exists(blog_dir):
        print(f"Error: {blog_dir} not found!")
        return 1

    # Read and combine all blog post markdown files
    print(f"Reading blog post files from {blog_dir}...")
    md_content = read_all_posts(blog_dir)

    print("Converting markdown to HTML...")
    content_html = convert_markdown_to_html(md_content)

    print("Generating full HTML page...")
    full_html = create_html_page(content_html)

    # Write the output file
    print(f"Writing to {html_file}...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print("Build complete!")
    return 0


if __name__ == '__main__':
    exit(main())

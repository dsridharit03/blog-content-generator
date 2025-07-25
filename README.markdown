# Blog Content Generator

A full-stack Python application that generates SEO-optimized blog posts based on user inputs (topic, category, region) using PyTrends for trending keywords and OpenAI for content generation.

## Setup
1. Activate virtual environment:
   ```powershell
      Step 1:
      cd C:\Sridhar\Python\AI_Projects\blog-content-generator
      step 2:
      python -m venv .venv_blog
      step 3:
      .\.venv_blog\Scripts\Activate


Install dependencies:pip install -r requirements.txt


Set OpenAI API key:$env:OPENAI_KEY = "your-openai-api-key"


Run the application:python analytics_generator.py


Open http://localhost:5000 in your browser.

live
 ## https://dsridharit03.github.io/blog-content-generator/

Features

Frontend: Bootstrap-styled form with loading indicator for topic, category, and region input.
Backend: Flask with PyTrends and OpenAI integration.
Generates 500-word SEO-optimized blog posts with trending keywords.
Saves analytics to SQLite database (analytics.db).
Supports PDF export of generated analytics.
Displays saved analytics with view/delete functionality and category filter at /analytics.
Includes input validation, error handling, and PyTrends retry logic.

Usage

Enter a topic (e.g., "machine learning"), select a category (e.g., "Technology"), and region (e.g., "US").
The app fetches trending keywords using PyTrends (or uses fallback keywords) and generates a blog post using OpenAI's GPT-4o model.
View the generated analytics and keywords, download as a PDF, or view/delete saved analytics at /analytics.

Portfolio Notes

Demonstrates full-stack development with Flask, HTML, CSS, JavaScript, and Bootstrap.
Integrates external APIs (PyTrends, OpenAI) for real-time data and AI-driven content.
Includes SQLite for data persistence and ReportLab for PDF generation.
Features robust error handling, retry logic, and input validation.



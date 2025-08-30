🤖 AI-Powered Blog Content Generator
A sophisticated Flask web application that leverages Google Trends data and OpenAI's GPT-4 to generate SEO-optimized, region-specific blog content. This tool helps content creators and marketers quickly produce relevant articles based on current trending topics.

https://img.shields.io/badge/Flask-2.3.3-green?logo=flask
https://img.shields.io/badge/OpenAI-GPT--4o-purple?logo=openai
https://img.shields.io/badge/Database-SQLite3-blue?logo=sqlite
https://img.shields.io/badge/License-MIT-yellow

✨ Features
📈 Trend-Integrated Content: Fetches real-time trending keywords for any topic using the PyTrends API.

🌍 Region & Category Specific: Generates content tailored to a specific geographic region and content category (e.g., Technology, Health, Finance).

🤖 AI-Powered Writing: Utilizes OpenAI's powerful GPT-4o model to create well-structured, engaging, and informative blog posts.

💾 Content Management: Automatically saves all generated blogs to a local SQLite database for later review and analysis.

📄 Export Functionality: Download your generated blog as a professionally formatted PDF or copy the text to your clipboard.

📊 Analytics Dashboard: View, filter, and manage all your saved blog posts in a simple web interface.



🛠️ Technology Stack
Component	Technology
Backend Framework	Flask (Python)
AI Language Model	OpenAI GPT-4o API
Trend Data	Google Trends via pytrends
Database	SQLite3
PDF Generation	ReportLab
Frontend	HTML5, Bootstrap 5, Vanilla JS
Styling	Custom CSS + Bootstrap

📁 Project Structure
🏗️ Architecture & Workflow

blog-content-generator/
├── templates/                 # Frontend HTML Templates
│   ├── index.html            # Main page with blog generation form
│   └── analytics.html        # Dashboard to view saved blogs
├── blog_generator.py         # Main Flask application & logic
├── config.py                 # Flask configuration settings
├── requirements.txt          # Python dependencies
├── test_openai.py           # Script to test OpenAI API connection
├── test_sqlite.py           # Script to test database functionality
└── analytics.db             # SQLite database (created after first run)

🚀 Getting Started
Prerequisites
Python 3.8+

An OpenAI API Key (Get one here)

Pip (Python package manager)

Installation & Setup
Clone the Repository


git clone https://github.com/dsridharit03/blog-content-generator.git
cd blog-content-generator
Create a Virtual Environment (Recommended)


python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install Dependencies


pip install -r requirements.txt
Set Up Your Environment Variable

Create a new environment variable named OPENAI_API_KEY.

Set its value to your secret OpenAI API key.

Important: For security, never commit your API key to version control. The app is configured to read it from the environment.

Run the Application


python blog_generator.py
The server will start at http://127.0.0.1:5000. Open this URL in your browser.

**Blog Content Search**
![Blog_Contnet_Search](https://github.com/user-attachments/assets/f7058b05-9370-47c2-96fc-cbd6f20b0f9e)

**Output**
![Blog_Contnet_Output](https://github.com/user-attachments/assets/df590da8-7e47-410c-9734-b0d181fad24d)



🎯 How to Use
Generate a Blog:

On the homepage, enter a Topic (e.g., "Renewable Energy").

Select a Category (e.g., "Science" or "Technology").

Choose a Region (e.g., "US" for United States).

Click "Generate Blog". The app will fetch trends and create content in seconds.

Manage Content:

View Saved Blogs: Click "View Saved Blogs" to see all your generated content in a table.

Filter: Use the category dropdown to filter blogs.

Read: Click "View" to read a full blog in a modal.

Delete: Remove blogs you no longer need.

Download Database: Get a copy of your entire analytics database.

Export:

After generation, use "Download as PDF" to get a formatted document.

Use "Copy Content" to quickly paste the markdown text into any CMS.

🔧 API Integration Details
Google Trends (pytrends): Used to find the top 5 related, trending queries for a given topic in a specific region and category. This ensures the generated content is relevant and SEO-friendly.

OpenAI GPT-4o: The core engine that writes the blog. It receives a carefully crafted prompt including the topic, category, region, keywords, and strict formatting instructions to produce high-quality, structured markdown output.

🤝 Contributing
Contributions are welcome! If you have ideas for new features, improvements, or find any bugs, please feel free to:

Fork the Project.

Create your Feature Branch (git checkout -b feature/AmazingFeature).

Commit your Changes (git commit -m 'Add some AmazingFeature').

Push to the Branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙋‍♂️ Author
Sridhar D

GitHub: @dsridharit03

Project Link: https://github.com/dsridharit03/blog-content-generator

💡 Future Enhancements
User Authentication & Personal Blogs.

Scheduled Trend Analysis.

Enhanced PDF Templates.

Social Media Snippet Generation.

Plagiarism Check Integration.

Dockerization for easy deployment.


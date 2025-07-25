from flask import Flask, render_template, request, jsonify, send_file
import config
from pytrends.request import TrendReq
from openai import OpenAI
import os
import time
import sqlite3
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

app = Flask(__name__)
app.config.from_object(config.config['development'])

# Initialize PyTrends
pytrends = TrendReq(hl='en-US', tz=360)

# Initialize OpenAI client
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define absolute path for database
DB_PATH = os.path.join('C:\\Sridhar\\Python\\AI_Projects\\blog-content-generator', 'analytics.db')

def get_keywords(topic, category, region):
    topic = topic.strip().lower()
    print(f"Fetching keywords for topic: '{topic}', category: '{category}', region: '{region}'")

    category_mapping = {
        'All': 0,
        'Business': 3,
        'Technology': 5,
        'Health': 45,
        'Sports': 20,
        'Science': 174,
        'Entertainment': 24,
        'Travel': 67,
        'Finance': 7,
        'Food & Drink': 71,
    }

    cat_code = category_mapping.get(category, 0)
    print(f"Using category code: {cat_code}")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            pytrends.build_payload(
                kw_list=[topic],
                cat=cat_code,
                timeframe='now 30-d',
                geo=region,
                gprop=''
            )
            related_queries = pytrends.related_queries()
            print(f"PyTrends related_queries response: {related_queries}")
            if (
                related_queries and topic in related_queries and
                related_queries[topic] and 'top' in related_queries[topic] and
                related_queries[topic]['top'] is not None
            ):
                keywords = related_queries[topic]['top']['query'].head(5).tolist()
                print(f"Successfully fetched keywords: {keywords}")
                return keywords
            else:
                print(f"No valid related queries for '{topic}' in '{region}', trying suggestions")
                suggestions = pytrends.suggestions(keyword=topic)
                print(f"PyTrends suggestions response: {suggestions}")
                if suggestions:
                    keywords = [s['title'] for s in suggestions[:5]]
                    print(f"Successfully fetched suggestions: {keywords}")
                    return keywords
                print(f"No suggestions found for '{topic}' in '{region}'")
        except Exception as e:
            print(f"PyTrends error: {e}, attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(60)
            continue

    print(f"Failed to fetch keywords for '{topic}', using fallback keywords")
    return [topic, f"{topic} guide", f"{topic} basics"]


def save_blog(topic, category, region, content, keywords):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Create table with correct schema
        cursor.execute('''CREATE TABLE IF NOT EXISTS analytics
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          topic TEXT,
                          category TEXT,
                          region TEXT,
                          content TEXT,
                          keywords TEXT)''')
        # Check if content column exists and add it if not
        cursor.execute("PRAGMA table_info(analytics)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'content' not in columns:
            cursor.execute("ALTER TABLE analytics ADD COLUMN content TEXT")
        # Insert data
        cursor.execute('''INSERT INTO analytics (topic, category, region, content, keywords)
                         VALUES (?, ?, ?, ?, ?)''',
                       (topic, category, region, content, ','.join(keywords)))
        conn.commit()
        print(f"Blog saved successfully for topic: '{topic}' at {DB_PATH}")
    except Exception as e:
        print(f"SQLite error in save_blog: {str(e)}")
    finally:
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blogs')
def view_blogs():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, topic, category, region, keywords, content FROM analytics')
        blogs = cursor.fetchall()
        conn.close()
        print(f"Fetched {len(blogs)} blogs from database")  # Debug
        return render_template('analytics.html', analytics=blogs)
    except Exception as e:
        print(f"Error in view_blogs: {str(e)}")
        return render_template('analytics.html', analytics=[])

@app.route('/generate-blog', methods=['POST'])
def generate_blog():
    try:
        topic = request.form['topic']
        category = request.form['category']
        region = request.form['region']

        if len(topic.strip()) < 3:
            return jsonify({'status': 'error', 'message': 'Topic must be at least 3 characters long'})
        category_mapping = {
            '0': 'All',
            '3': 'Business',
            '5': 'Technology',
            '7': 'Finance',
            '20': 'Sports',
            '24': 'Entertainment',
            '45': 'Health',
            '67': 'Travel',
            '71': 'Food & Drink',
            '174': 'Science'
        }
        category = category_mapping.get(category, 'All')

        keywords = get_keywords(topic,category, region)

        prompt = f"""
        Write a 500-word blog post on the topic '{topic}' in the category '{category}' tailored for the region '{region}'. 
        Incorporate the following trending keywords: {', '.join(keywords)}. 

        Structure the content as follows:
        1. Main Title (clear and engaging)
        2. Introduction paragraph
        3. 2-3 main sections with descriptive headings
        4. Conclusion paragraph

        Formatting guidelines:
        - Use Markdown formatting
        - Main title should be preceded by # 
        - Section headings should be preceded by ## 
        - Separate paragraphs with blank lines
        - Keep sentences concise and paragraphs short (2-3 sentences each)
        - Use bullet points where appropriate

        Ensure the content is engaging, informative, and optimized for SEO with a clear structure.
        Use a friendly and professional tone suitable for a general audience.
        """

        print(f"Calling OpenAI API for topic: '{topic}'")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a skilled content writer creating SEO-optimized blog posts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
            timeout=30
        )
        print("OpenAI API call successful")
        blog_content = response.choices[0].message.content

        print("Attempting to save blog to database")
        save_blog(topic, category, region, blog_content, keywords)

        return jsonify({
            'status': 'success',
            'blog_content': blog_content,
            'keywords': keywords
        })

    except Exception as e:
        print(f"Error in generate_blog: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# @app.route('/download-blog', methods=['POST'])
# def download_blog():
#     try:
#         content = request.form['content']
#         print(f"Raw content for PDF: {content[:100]}...")  # Debug
#         # Replace <br> with \n for ReportLab compatibility
#         cleaned_content = content.replace('<br>', '\n')
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter)
#         styles = getSampleStyleSheet()
#         story = [Paragraph(cleaned_content, styles['Normal'])]
#         doc.build(story)
#         buffer.seek(0)
#         print("PDF generated successfully")
#         return send_file(buffer, as_attachment=True, download_name='blog.pdf')
#     except Exception as e:
#         print(f"Error in download_blog: {str(e)}")
#         return jsonify({'status': 'error', 'message': str(e)})


@app.route('/download-blog', methods=['POST'])
def download_blog():
    try:
        content = request.form['content']
        print(f"Raw content for PDF: {content[:100]}...")  # Debug
        
        # Create a BytesIO buffer for the PDF
        buffer = BytesIO()
        
        # Create the PDF document with margins to match webpage
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=1*inch, bottomMargin=1*inch)
        
        # Define styles to match index.html
        styles = getSampleStyleSheet()
        
        styles.add(ParagraphStyle(
            name='BlogTitle',
            fontName='Helvetica-Bold',
            fontSize=16,  # 2rem ≈ 16pt
            leading=20,
            alignment=1,  # Center
            textColor=HexColor('#2c3e50'),  # .blog-title
            spaceAfter=12
        ))
        
        styles.add(ParagraphStyle(
            name='BlogSectionTitle',
            fontName='Helvetica-Bold',
            fontSize=12,  # 1.5rem ≈ 12pt
            leading=16,
            alignment=0,  # Left
            textColor=HexColor('#3498db'),  # .blog-section-title
            spaceBefore=12,
            spaceAfter=8
        ))
        styles.add(ParagraphStyle(
            name='BlogContent',
            fontName='Helvetica',
            fontSize=9,  # 1.1rem ≈ 9pt
            leading=12,  # Line-height 1.6
            alignment=4,  # Justify
            spaceAfter=8
        ))
        
        styles.add(ParagraphStyle(
            name='BlogIntro',
            fontName='Helvetica-Oblique',  # Italic
            fontSize=9,
            leading=12,
            alignment=4,  # Justify
            textColor=HexColor('#555555'),  # .blog-intro
            spaceAfter=12
        ))
        
        styles.add(ParagraphStyle(
            name='BlogListItem',
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            alignment=0,  # Left
            leftIndent=20,
            firstLineIndent=-10,
            spaceAfter=4
        ))
        
        # Process the content
        elements = []
        is_first_paragraph = True
        lines = content.split('\n')
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('# '):
                elements.append(Paragraph(line[2:], styles['BlogTitle']))
                elements.append(Spacer(1, 0.5*inch))
                is_first_paragraph = True
                in_list = False
            elif line.startswith('## '):
                elements.append(Paragraph(line[3:], styles['BlogSectionTitle']))
                elements.append(Spacer(1, 0.2*inch))
                is_first_paragraph = False
                in_list = False
            elif line.startswith('### '):
                elements.append(Paragraph(line[4:], styles['BlogSectionTitle']))
                elements.append(Spacer(1, 0.1*inch))
                is_first_paragraph = False
                in_list = False
            elif line.startswith('- '):
                elements.append(Paragraph("• " + line[2:], styles['BlogListItem']))
                elements.append(Spacer(1, 0.1*inch))
                is_first_paragraph = False
                in_list = True
            else:
                if in_list:
                    elements.append(Spacer(1, 0.2*inch))
                    in_list = False
                if is_first_paragraph:
                    elements.append(Paragraph(line, styles['BlogIntro']))
                    is_first_paragraph = False
                else:
                    elements.append(Paragraph(line, styles['BlogContent']))
                elements.append(Spacer(1, 0.2*inch))
        
        doc.build(elements)
        buffer.seek(0)
        print("PDF generated successfully")
        return send_file(buffer, as_attachment=True, download_name='blog.pdf')
    except Exception as e:
        print(f"Error in download_blog: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/delete-blog/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM analytics WHERE id = ?', (blog_id,))
        conn.commit()
        print(f"Blog ID {blog_id} deleted successfully")
        conn.close()
        return jsonify({'status': 'success', 'message': 'Blog deleted'})
    except Exception as e:
        print(f"Error in delete_blog: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
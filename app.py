from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, ShortenedURL
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        
        if not original_url:
            flash('Please enter a URL', 'error')
            return redirect(url_for('index'))
        
        # Add http:// if missing
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url
        
        # Check if URL already exists
        existing_url = ShortenedURL.query.filter_by(original_url=original_url).first()
        
        if existing_url:
            short_url = request.host_url + existing_url.short_code
            flash('URL already shortened!', 'info')
        else:
            # Create new shortened URL
            new_url = ShortenedURL(original_url=original_url)
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + new_url.short_code
            flash('URL shortened successfully!', 'success')
        
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_entry = ShortenedURL.query.filter_by(short_code=short_code).first_or_404()
    
    # Increment click counter
    url_entry.clicks += 1
    db.session.commit()
    
    return redirect(url_entry.original_url)

@app.route('/stats')
def stats():
    urls = ShortenedURL.query.order_by(ShortenedURL.created_at.desc()).all()
    return render_template('stats.html', urls=urls)

@app.route('/delete/<int:url_id>')
def delete_url(url_id):
    url_entry = ShortenedURL.query.get_or_404(url_id)
    db.session.delete(url_entry)
    db.session.commit()
    flash('URL deleted successfully!', 'success')
    return redirect(url_for('stats'))

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
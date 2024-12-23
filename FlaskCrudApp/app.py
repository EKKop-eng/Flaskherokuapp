
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use DATABASE_URL environment variable for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///items.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Home: List all items
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

# Add a new item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit an item
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

# Delete an item
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', item=item)

if __name__ == '__main__':
    # Create database tables if not already created (useful for local testing)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

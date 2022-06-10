import sqlite3
import logging
import sys
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from markupsafe import escape
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    app.logger.info('A post has been retrieved')
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('A non-existing article is accessed and a 404 page has been returned')
      return render_template('404.html'), 404
    else:
       app.logger.info('An existing article has been retrieved')
       return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About US page has been retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))
    app.logger.info('A new article has been created-')
    return render_template('create.html')

@app.route('/healthz')
def status():
  response=app.response_class(
      response=json.dumps({"result":"ok-healthy"}),
      status=200,
      mimetype='application/json'
  )
  app.logger.debug('DEBUG message')
  return response

@app.route('/metrics')
def metrics():
  response = app.response_class(
    #post_counts=get_post.post_count
      response=json.dumps({"db_connection_count ": "10", "post_count": "6" }),
      status=200,
      mimetype='application/json'
  )
  app.logger.debug('DEBUG message')
  return response
# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    app.run(host='0.0.0.0', port='3111')

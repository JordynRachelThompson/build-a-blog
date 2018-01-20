from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:mypassword@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(500))
    
    def __init__(self, title, body ):
        self.title = title
        self.body = body
        
@app.route('/blog', methods=['GET'])
def blog():

    blogs = Blog.query.all()
    retrieve_id = ""
    retrieve_id = request.args.get('id')
    if retrieve_id is None:
        return render_template('blog.html', title="Build-a-Blog", blogs=blogs)
    else:
        post = Blog.query.filter_by(id=retrieve_id).first()
        title = post.title
        body = post.body 

        return render_template('entry.html', retrieve_id=retrieve_id, title=title, body=body)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == "POST":
        title = request.form['title']
        body = request.form['body'] 
        title_error = ''
        entry_error = ''      

        if title == '':
            title_error = "Please enter a title"
            return render_template('newpost.html', title_error=title_error, entry_error=entry_error, title=title, body=body)
        if body == '':
            entry_error = "Please enter text"
            return render_template('newpost.html', title_error=title_error, entry_error=entry_error, title=title, body=body)
        if not title_error and not entry_error:
            new_entry = Blog(title, body)
            db.session.add(new_entry)
            db.session.flush()
            db.session.commit()
            post = Blog.query.filter_by(id=new_entry.id).first()
            title = post.title
            body = post.body
            
            return render_template('entry.html', title=title, body=body)
    return render_template('newpost.html')             

if __name__ == "__main__":
    app.run()
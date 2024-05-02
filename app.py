from flask import Flask, render_template, request, url_for, redirect 
from flask_sqlalchemy import SQLAlchemy  


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py') 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	todo = db.Column(db.String(200))


	def __str__(self):
		return f"{self.todo}"



@app.route('/', methods=['GET', 'POST'])
def home():
	todos = Todo.query.all()
	if request.method == 'POST':
		todo1 = request.form.get('todo')
		todo2 = Todo(todo=todo1)
		db.session.add(todo2)
		db.session.commit()
		return redirect(request.url)

	return render_template("home.html", todos=todos)



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_todo(id):
	todo = Todo.query.filter_by(id=id).first()
	if request.method == 'POST':
		todo.todo = request.form.get('todo')
		db.session.commit()
		return redirect(url_for('home'))
	return render_template("update_todo.html", todo=todo)



@app.route('/delete/<int:id>')
def delete_todo(id):
	todo = Todo.query.filter_by(id=id).first()
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for('home'))





if __name__ == '__main__':
	app.run(port=3000)
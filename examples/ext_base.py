from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Something(Base):
    __tablename__ = 'something'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(255), unique=True)

    rel = relationship('Something')
    rel_dynamic = relationship('Something', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
db = SQLAlchemy(app)

class A(db.Model):
    __tablename__ = 'a'
    id = db.Column(db.Integer, primary_key=True)
    b = db.relationship('B')
    b_dynamic = db.relationship('B', lazy='dynamic')

class B(db.Model):
    __tablename__ = 'b'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('a.id'))
    user = db.relationship('A')

db.register_base(Base)
db.create_all()

@app.before_first_request
def insert_user():
    # We can create new objects the normal way
    user = User(id=1, username='foo', email='foo@bar.com')
    db.session.add(user)

    a = A(id=1)
    db.session.add(a)
    db.session.commit()

@app.route('/<int:user_id>')
def index(user_id):
    # # Or we can using the model's query property
    user = User.query.get_or_404(user_id)


    print("User.query", type(User.query))
    print("Something.query", type(Something.query))
    print("user.rel", type(user.rel))
    print("user.rel_dynamic", type(user.rel_dynamic))

    a = A.query.first_or_404()
    print("A.query", type(A.query))
    print("B.query", type(B.query))
    print("a.b", type(a.b))
    print("a.b_dynamic", type(a.b_dynamic))

    print(user.rel_dynamic.paginate())
    # print(a.b_dynamic.paginate())

    return "Hello, {}".format(a.id)

if __name__ == '__main__':
    app.run(debug=True)

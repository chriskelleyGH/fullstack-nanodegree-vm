from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    items = session.query(Item).filter().order_by('Item.id desc')
    return render_template('catalog.html', categories=categories, items=items)

@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'], category_id=request.form['category'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        categories = session.query(Category).all()
        return render_template('newitem.html', categories=categories)

@app.route('/catalog/category/<int:category_id>/items/')
def showItems(category_id):
    return 'This page will be for showing the items for each category'

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
    return 'This page will be for showing item %s' % item_id

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/edit/')
def editItem(item_id):
    return 'This page will be for editing item %s' % item_id

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/delete/')
def deleteItem(item_id):
    return 'This page will be for deleting item %s' % item_id

@app.route('/catalog/JSON/')
def catalogJSON():
    return 'This page will be for the catalog json endpoint'

@app.route('/catalog/category/<int:category_id>/JSON/')
def categoryJSON(category_id):
    return 'This page will be for category %s json endpoint' % category_id

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/JSON/')
def itemJSON(category_id, item_id):
    return 'This page will be for item %s json endpoint' % item_id



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

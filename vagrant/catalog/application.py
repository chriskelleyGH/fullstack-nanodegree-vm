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

@app.route('/catalog/category/<int:category_id>/')
@app.route('/catalog/category/<int:category_id>/items/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template('items.html', items=items, category=category)

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template ('item.html', item=item, category=category)

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        categories = session.query(Category).all()
        return render_template('edititem.html', category_id=category_id, item_id=item_id, item=editedItem, categories=categories)

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteitem.html', category_id=category_id, item_id=item_id, item=itemToDelete)


@app.route('/catalog/JSON/')
def catalogJSON():
    return 'This page will be for the catalog json endpoint'


@app.route('/catalog/category/<int:category_id>/JSON/')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/JSON/')
def itemJSON(category_id, item_id):
    Catalog_Item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Catalog_Item=Catalog_Item.serialize)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

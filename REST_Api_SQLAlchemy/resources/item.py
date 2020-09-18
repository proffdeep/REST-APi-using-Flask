from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
						type=float,
						required=True,
						help="This field cannot be left blank!"
						)

	parser.add_argument('store_id',
						type=int,
						required=True,
						help="Every item needs a store_id."
						)

	@jwt_required()
	def get(self,name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message':'Item not found'}, 404

	def post(self,name):
		if ItemModel.find_by_name(name):
			return {'message':"already exists"}

		data = Item.parser.parse_args()
		item = ItemModel(name,**data)
		try:
			item.save_to_db()
		except:
			return {'message':'error occured'}

		return item.json(), 201

	def delete(self,name):
		item = ItemModel.find_by_name(name)
		
		if item:
			item.delete_from_db()
			return {"message":"item deleted"}

		return {"message": "Item not found"},404

	def put(self,name):
		item = ItemModel.find_by_name(name)
		data = self.parser.parse_args()

		if item:
			item.price = data['price']
		else:
			item = ItemModel(name,**data)

		item.save_to_db()
		return item.json()


class ItemList(Resource):
	def get(self):
		return {'items': list(map(lambda x: x.json() , ItemModel.query.all()))}
		



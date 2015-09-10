from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask.ext.cors import CORS
import json

from flask import Flask, request, Response, render_template

app = Flask(__name__)
CORS(app)

connection = MongoClient('localhost', 27017)
db = connection.mydb
imoveis = db.imoveis
estados = db.estados
cidades = db.cidades
bairros = db.bairros

def toJson(data):
	return json.dumps(data, default=json_util.default)

@app.route('/buscarImoveisPorGeoLocalizacao', methods=['POST'])
def buscarImoveisPorGeoLocalizacao():
	req_json = request.get_json()
	print (req_json)
	results = imoveis.find({"$and":[
		{"loc" : {"$within" : {"$box" : req_json['location']}}},
		{"tipo" : {"$in": req_json['tipos']}},
		{"operacao" : req_json['operacao']}
		]})

	json_results = []
	for result in results:
		json_results.append(result)

	resp = Response(
		response=toJson(json_results), status=200, mimetype="application/json")
	return resp

@app.route('/buscarImoveisPorFiltro', methods=['POST'])
def buscarImoveisPorFiltro():
	req_json = request.get_json()
	print (req_json)
	results = imoveis.find({"$and":[
		{"loc" : {"$within" : {"$box" : req_json['location']}}},
		{"tipo" : {"$in": req_json['tipos']}},
		{"operacao" : req_json['operacao']}
		]})

	json_results = []
	for result in results:
		json_results.append(result)

	resp = Response(
		response=toJson(json_results), status=200, mimetype="application/json")
	return resp

@app.route('/buscarEstados', methods=['POST'])
def buscarEstados():
	req_json = request.get_json()
	print (req_json)
	results = estados.find()

	json_results = []
	for result in results:
		json_results.append(result)

	resp = Response(
		response=toJson(json_results), status=200, mimetype="application/json")
	return resp

@app.route('/buscarCidadesPorEstado', methods=['POST'])
def buscarCidadesPorEstado():
	req_json = request.get_json()
	print (req_json)
	results = cidades.find({"estado" : req_json['estado']})

	json_results = []
	for result in results:
		json_results.append(result)

	resp = Response(
		response=toJson(json_results), status=200, mimetype="application/json")
	return resp

@app.route('/buscarBairrosPorEstadoECidade', methods=['POST'])
def buscarBairrosPorEstadoECidade():
	req_json = request.get_json()
	print (req_json)
	results = bairros.find({"cidade" : req_json['cidade']})

	json_results = []
	for result in results:
		json_results.append(result)

	resp = Response(
		response=toJson(json_results), status=200, mimetype="application/json")
	return resp

if __name__ == '__main__':
    app.run(debug=True)
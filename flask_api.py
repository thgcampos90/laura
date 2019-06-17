from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/thiago"
mongo = PyMongo(app)

@app.route('/', methods=['GET','POST','DELETE'])
def index():
    return 'Nenhuma operacao realizada.'

#Etapa 1 - GET

@app.route('/exercise_1/<string:varModalidade>/<varDataIni>/<varDataFim>', methods=['GET'])
def exercise_1(varModalidade, varDataIni, varDataFim):
    result = mongo.db.estudantes.find({"$and":[{"data_inicio": {"$gte": varDataIni,"$lte": varDataFim}},{"modalidade": varModalidade}]}).sort([("data_inicio", -1)])
    return dumps(result)

@app.route('/exercise_2/<string:varCampus>', methods=['GET'])
def exercise_2(varCampus):
    return jsonify(mongo.db.estudantes.distinct("curso",{"campus": varCampus}));

@app.route('/exercise_3/<string:varCampus>/<varDataIni>/<varDataFim>', methods=['GET'])
def exercise_3(varCampus, varDataIni, varDataFim):
    return jsonify({'totalAlunos': len(mongo.db.estudantes.distinct("nome", {"$and":[{"data_inicio": {"$gte": varDataIni,"$lte": varDataFim}},{"campus": varCampus}]}))})

#Etapa 2 - POST

@app.route('/exercise_4', methods=['POST'])
def exercise_4():
    req_data = request.get_json()
    
    aluno = {"nome": req_data["nome"], "idade_ate_31_12_2016": req_data["idade_ate_31_12_2016"], "ra": req_data["ra"], "campus": req_data["campus"], "municipio": req_data["municipio"], "curso": req_data["curso"], "modalidade": req_data["modalidade"], "nivel_do_curso": req_data["nivel_do_curso"], "data_inicio": req_data["data_inicio"]}
    mongo.db.estudantes.insert_one(aluno)
    return Response(dumps(aluno), status=201, mimetype='application/json')

@app.route('/exercise_5/<string:varRa>/<string:varCampus>', methods=['DELETE'])
def exercise_5(varRa,varCampus):
    mongo.db.estudantes.delete_many({"ra":varRa,"campus":varCampus})
    return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

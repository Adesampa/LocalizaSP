# app.py
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    return conn

def query_database(query, lat, lon):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(query, (lat, lon))
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result

@app.route('/distritos', methods=['GET'])
def distritos():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Forneça a Latitude e Longitude'}), 400

    query = '''
    SELECT 
        ds_nome
    FROM 
        distritos
    WHERE 
        ST_Contains(
            geom, 
            ST_FlipCoordinates(ST_SetSRID(ST_MakePoint(%s, %s), 4326))
        );
    '''

    result = query_database(query, lat, lon)

    if result:
        return jsonify({'Distrito': result[0]})
    else:
        return jsonify({'error': 'Coordenadas não encontradas nos distritos da cidade de São Paulo.'}), 404

@app.route('/subprefeituras', methods=['GET'])
def subprefeituras():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Forneça a Latitude e Longitude'}), 400

    query = '''
    SELECT 
        ds_subpref
    FROM 
        distritos
    WHERE 
        ST_Contains(
            geom, 
            ST_FlipCoordinates(ST_SetSRID(ST_MakePoint(%s, %s), 4326))
        );
    '''

    result = query_database(query, lat, lon)

    if result:
        return jsonify({'Subprefeitura': result[0]})
    else:
        return jsonify({'error': 'Coordenadas não encontradas nas subprefeituras da cidade de São Paulo.'}), 404
    
@app.route('/distritos_subprefeituras', methods=['GET'])
def distrito_subprefeitura():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Forneça a Latitude e Longitude'}), 400

    query = '''
    SELECT 
        ds_nome, ds_subpref
    FROM 
        distritos
    WHERE 
        ST_Contains(
            geom, 
            ST_FlipCoordinates(ST_SetSRID(ST_MakePoint(%s, %s), 4326))
        );
        
    '''
    result = query_database(query, lat, lon)

    if result:
        return jsonify({'Distrito': result[0], 'Subprefeitura': result[1]})
    else:
        return jsonify({'error': 'Coordenadas não encontradas na cidade de São Paulo.'}), 404

@app.route('/', methods=['GET'])
def api_status():
    return jsonify({'status': 'API está funcionando corretamente'}), 200

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# api.py
from flask import Flask, request, jsonify
import psycopg2
import os
import logging
from psycopg2 import OperationalError

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do Flask baseada em variáveis de ambiente
flask_env = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = flask_env == 'development'

def validate_coordinates(lat, lon):
    """Valida se as coordenadas são números válidos e estão dentro de limites razoáveis"""
    try:
        lat_float = float(lat)
        lon_float = float(lon)
        
        # Verificar limites razoáveis para São Paulo
        # São Paulo está aproximadamente entre:
        # Latitude: -24.0 a -23.0
        # Longitude: -47.0 a -46.0
        if not (-25.0 <= lat_float <= -22.0):
            return False, "Latitude fora dos limites esperados para São Paulo"
        if not (-48.0 <= lon_float <= -45.0):
            return False, "Longitude fora dos limites esperados para São Paulo"
            
        return True, (lat_float, lon_float)
    except (ValueError, TypeError):
        return False, "Coordenadas devem ser números válidos"

def get_db_connection():
    """Estabelece conexão com o banco de dados com tratamento de erro"""
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        return conn
    except OperationalError as e:
        logger.error(f"Erro ao conectar com banco de dados: {e}")
        raise

def query_database(query, lat, lon):
    """Executa query no banco com tratamento de erro"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(query, (lat, lon))
        result = cur.fetchone()

        cur.close()
        conn.close()

        return result
    except Exception as e:
        logger.error(f"Erro ao executar query: {e}")
        raise

@app.route('/distritos', methods=['GET'])
def distritos():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Forneça a Latitude e Longitude'}), 400

    # Validar coordenadas
    is_valid, result_or_error = validate_coordinates(lat, lon)
    if not is_valid:
        return jsonify({'error': result_or_error}), 400
    
    lat_float, lon_float = result_or_error

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

    try:
        result = query_database(query, lat_float, lon_float)
        if result:
            return jsonify({'Distrito': result[0]})
        else:
            return jsonify({'error': 'Coordenadas não encontradas nos distritos da cidade de São Paulo.'}), 404
    except Exception as e:
        logger.error(f"Erro ao consultar distritos: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/subprefeituras', methods=['GET'])
def subprefeituras():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Forneça a Latitude e Longitude'}), 400

    # Validar coordenadas
    is_valid, result_or_error = validate_coordinates(lat, lon)
    if not is_valid:
        return jsonify({'error': result_or_error}), 400
    
    lat_float, lon_float = result_or_error

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

    try:
        result = query_database(query, lat_float, lon_float)
        if result:
            return jsonify({'Subprefeitura': result[0]})
        else:
            return jsonify({'error': 'Coordenadas não encontradas nas subprefeituras da cidade de São Paulo.'}), 404
    except Exception as e:
        logger.error(f"Erro ao consultar subprefeituras: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
@app.route('/distritos_subprefeituras', methods=['GET'])
def distrito_subprefeitura():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Forneça a Latitude e Longitude'}), 400

    # Validar coordenadas
    is_valid, result_or_error = validate_coordinates(lat, lon)
    if not is_valid:
        return jsonify({'error': result_or_error}), 400
    
    lat_float, lon_float = result_or_error

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
    
    try:
        result = query_database(query, lat_float, lon_float)
        if result:
            return jsonify({'Distrito': result[0], 'Subprefeitura': result[1]})
        else:
            return jsonify({'error': 'Coordenadas não encontradas na cidade de São Paulo.'}), 404
    except Exception as e:
        logger.error(f"Erro ao consultar distrito e subprefeitura: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/', methods=['GET'])
def api_status():
    return jsonify({
        'status': 'API está funcionando corretamente',
        'version': '1.0.0',
        'endpoints': {
            'distritos': {
                'url': '/distritos',
                'method': 'GET',
                'parameters': ['lat', 'lon'],
                'example': '/distritos?lat=-23.55052&lon=-46.63331'
            },
            'subprefeituras': {
                'url': '/subprefeituras', 
                'method': 'GET',
                'parameters': ['lat', 'lon'],
                'example': '/subprefeituras?lat=-23.55052&lon=-46.63331'
            },
            'distritos_subprefeituras': {
                'url': '/distritos_subprefeituras',
                'method': 'GET', 
                'parameters': ['lat', 'lon'],
                'example': '/distritos_subprefeituras?lat=-23.55052&lon=-46.63331'
            },
            'health': {
                'url': '/health',
                'method': 'GET',
                'description': 'Health check endpoint'
            }
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check para monitoramento"""
    try:
        # Testa conexão com banco
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        logger.error(f"Health check falhou: {e}")
        return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 503

if __name__ == '__main__':
    # Configuração baseada em variável de ambiente
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)

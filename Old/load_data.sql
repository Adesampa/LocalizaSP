CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE IF NOT EXISTS distritos (
    id SERIAL PRIMARY KEY,
    ds_nome VARCHAR(255),
    ds_subpref VARCHAR(255),
    geom GEOMETRY(MULTIPOLYGON, 4326)
);

-- Importar o shapefile usando shp2pgsql com mais informações de debug
\! echo "Iniciando importação do shapefile..."
\! shp2pgsql -d -s 4326 -I /app/distritos/distritos.shp public.distritos | psql -U hugo -d adesampa
\! echo "Importação concluída. Verificando contagem de registros..."
\! echo "SELECT COUNT(*) FROM distritos;" | psql -U hugo -d adesampa

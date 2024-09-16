#!/bin/bash
set -e

echo "Aguardando o PostgreSQL iniciar..."

# Espera o PostgreSQL estar pronto para aceitar conexões
#until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"; do
#  sleep 2
#done

echo "Iniciando importação do shapefile..."

# Importa o shapefile usando o shp2pgsql
shp2pgsql -d -s 4326 -I /app/distritos/distritos.shp public.distritos | psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"

echo "Importação concluída."

# Verifica a contagem de registros
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT COUNT(*) FROM distritos;"

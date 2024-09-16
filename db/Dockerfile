FROM postgis/postgis:16-3.4

# Instala o shp2pgsql e outros utilitários necessários
RUN apt-get update && \
    apt-get install -y postgis && \
    rm -rf /var/lib/apt/lists/*

# Copia o script SQL e os shapefiles para o diretório apropriado
COPY load_data.sql /docker-entrypoint-initdb.d/
COPY distritos/ /app/distritos/
COPY import_shapefile.sh /docker-entrypoint-initdb.d/import_shapefile.sh
# LocalizaSP API

API de geolocalização para consulta de distritos e subprefeituras da cidade de São Paulo.

## Sumário

- [Descrição](#descrição)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Executar a Aplicação](#como-executar-a-aplicação)
- [Como Utilizar a API](#como-utilizar-a-api)
- [Exemplos de Uso](#exemplos-de-uso)
- [Parando os Contêineres](#parando-os-contêineres)
- [Limpeza](#limpeza-opcional)
- [Contribuição](#contribuição)
- [Problemas Conhecidos / FAQ](#problemas-conhecidos--faq)
- [Contato](#contato)
- [Licença](#licença)

## Descrição

A LocalizaSP API permite que usuários consultem, a partir de coordenadas geográficas, a qual distrito e subprefeitura essas coordenadas pertencem na cidade de São Paulo. A API utiliza um banco de dados PostgreSQL com extensão PostGIS para realizar consultas espaciais.

## Tecnologias Utilizadas

- Python 3.11
- Flask
- PostgreSQL 16 com PostGIS
- Docker e Docker Compose

## Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em sua máquina:

- Git
- Docker + Docker Compose **OU** Podman + podman-compose

### Configuração Adicional para WSL2 + Podman

Se você estiver usando Podman no WSL2, configure o firewall driver antes de executar:

Configure o Podman para usar `iptables` ao invés de `nftables` adicionando as seguintes linhas ao arquivo `/etc/containers/containers.conf`:

```ini
[network]
firewall_driver="iptables"

## Instalação

1. Clone o repositório:
   ```bash
   git clone git@github.com:Adesampa/LocalizaSP.git
   cd LocalizaSP
   ```

2. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
   
   Edite o arquivo `.env` e ajuste as configurações conforme necessário:
   - `POSTGRES_PASSWORD`: Defina uma senha segura para o banco
   - `API_PORT`: Porta da API (padrão: 8080)
   - `DB_PORT_EXTERNAL`: Porta externa do banco (padrão: 5433)
   - `FLASK_ENV`: development ou production

3. A estrutura do projeto deve ser a seguinte:
   ```
   ├── docker-compose.yml
   ├── api
   │   ├── api.py
   │   ├── requirements.txt
   │   └── [outros arquivos da API]
   └── db
       ├── Dockerfile
       ├── load_data.sql
       ├── import_shapefile.sh
       ├── distritos/
       │   └── distritos.shp
       │   └── [outros arquivos do shapefile]
       └── [outros arquivos do banco de dados]
   ```

## Como Executar a Aplicação

1. Na raiz do projeto, execute:

   **Com Docker:**
   ```bash
   docker-compose up --build
   ```

   **Com Podman:**
   ```bash
   podman compose up --build
   ```

2. Verifique se a API está funcionando acessando:

   http://localhost:8080/

## Como Utilizar a API

A API oferece os seguintes endpoints:

- `GET /`: Verifica o status da API e lista endpoints disponíveis
- `GET /health`: Endpoint de health check para monitoramento
- `GET /distritos?lat=<latitude>&lon=<longitude>`: Retorna o distrito
- `GET /subprefeituras?lat=<latitude>&lon=<longitude>`: Retorna a subprefeitura  
- `GET /distritos_subprefeituras?lat=<latitude>&lon=<longitude>`: Retorna o distrito e a subprefeitura

### Validação de Coordenadas

A API valida automaticamente:
- Se lat/lon são números válidos
- Se as coordenadas estão dentro dos limites de São Paulo
- Latitude entre -25.0 e -22.0
- Longitude entre -48.0 e -45.0

## Exemplos de Uso

1. **Verificar Status da API:**
   ```
   http://localhost:8080/
   ```

2. **Health Check:**
   ```
   http://localhost:8080/health
   ```

3. **Consultar Distrito:**
   ```
   http://localhost:8080/distritos?lat=-23.55052&lon=-46.63331
   ```

4. **Consultar Subprefeitura:**
   ```
   http://localhost:8080/subprefeituras?lat=-23.55052&lon=-46.63331
   ```

5. **Consultar Distrito e Subprefeitura:**
   ```
   http://localhost:8080/distritos_subprefeituras?lat=-23.55052&lon=-46.63331
   ```

## Segurança e Configuração

### Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configurações sensíveis:
- Credenciais do banco de dados não ficam expostas no código
- Senhas podem ser alteradas sem modificar o código
- Configuração de ambiente (development/production)

### Validação de Entrada

- Validação automática de coordenadas
- Verificação de limites geográficos
- Tratamento de erros robusto
- Logging de erros para debug

### Portas Não-Conflitantes

- API: porta 8080 (ao invés de 5000)
- PostgreSQL: porta 5433 (ao invés de 5432)
- Configurável via variáveis de ambiente

## Parando os Contêineres

Para parar os contêineres em execução, execute:

**Com Docker:**
```bash
docker-compose down
```

**Com Podman:**
```bash
podman compose down
```

## Limpeza (Opcional)

Para remover todos os contêineres, imagens e volumes associados ao projeto:

**Com Docker:**
```bash
docker-compose down --rmi all --volumes
```

**Com Podman:**
```bash
podman compose down --rmi all --volumes
```

> **Atenção**: Isso irá remover todos os dados armazenados no banco de dados.


## Problemas Conhecidos / FAQ

### Problemas de Rede com Podman no WSL2

Se você estiver usando Podman no WSL2 e encontrar erros relacionados ao `nftables` como:
```
Error: netavark: nftables error: nft did not return successfully while applying ruleset
```

**Solução**: Configure o Podman para usar `iptables` ao invés de `nftables` adicionando as seguintes linhas ao arquivo `/etc/containers/containers.conf`:

```ini
[network]
firewall_driver="iptables"
```

Após fazer essa alteração, reinicie o WSL2 ou execute `podman system reset` para aplicar as mudanças.

### Outros Problemas Comuns

- **P: A API não retorna os dados para algumas coordenadas. Por quê?**
  R: Certifique-se de que as coordenadas fornecidas estão dentro dos limites da cidade de São Paulo.

- **P: Como posso adicionar novos distritos ou subprefeituras?**
  R: Atualize o arquivo shapefile na pasta `db/distritos/` e reconstrua os contêineres Docker.

- **P: Erro "no container with name or ID found"**
  R: Execute `podman compose down --volumes` para limpar containers antigos e tente novamente.



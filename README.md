# Agente facilitador de negócios
Agente facilitador para fechamento de negócios, utilizando de diversas tecnologias para as mais diversas personalidades dos clientes.

## Propósito
O objetivo deste projeto é facilitar a intereção entre colaboradores de agências de crédito cooperativitas com seus cooperados, Verificando as personalidades de cada colaborados, cooperado juntamente com seus históricos (créditos aprovados, feedbacks anteriores, compras). Foi utilizado um agente de IA para fazer a análise em Json de todos os dados, e dessa maneira ele retorna uma lista de colaboradores em ordem do mais indicado para o menos indicado. Também retorna assuntos que podem ser puxados e quais evitar para garantir melhor conexão entre colaborador e cooperado.

## Funcionalidades aplicadas
- Integração com IA para análise de personalidade
- Assíncrono
- Filas
- Autenticação e validação com token
- Microserviços (Front End, Worker, API Rest)
- Front-end estático
- Criptografia Front<->Back e Back<->Infra

## Tecnologias Utilizadas
- Backend:
    - Python FaspApi
    - Arquiterura Hexagonal
    - boto3
    - uvicorn

- Frontend:
    - Vue 3
    - Bootstrap
    - Axios
    - Vite
    - Typescript
    
- Infraestrutura:
    - Docker
    - PostgreSQL
    - Redis
    - Nginx
    - GCP Storages
    - GCP Machine
    - AWS Bedrock agent

## Instalação
### Pré-requisitos obrigatórios
- Docker ^25.0.3
- Python ^3.10

### Pré-requisitos para desenvolvimento
- Docker ^25.0.3
- Node ^18
- Python ^3.10

### Clonando o Repositório

```bash
git clone https://github.com/CiprianoLucas/ConsultoraAila.git
cd ConsultoraAila
```

## Configuração obrigatória
**Essa aplicação utiliza um agente de IA da AWS Bedrock, crie e anote as credênciais IAM e do Agente**

Configure as variáveis de ambiente necessárias, como credenciais do banco de dados e chaves secretas, utilize os arquivos example.env para criar um .env

Crie um arquivo .env em /front/aila com:

VITE_API=http://localhost:8000

Certifique-se de que o backend e o frontend estejam apontando para os respectivos servidores e endpoints.

### Configurando o ambiente para desenvolvimento
Com docker em funcionamento, execute o comando para criar o container
```bash
docker compose up -d --build
```

O projeto foi feito levando em consideração uma base de dados existente pela cooperativa. Aqui vamos simular com um banco de dados. Um banco Postgree foi criado no docker, pode ser gerado as tabelas e dados com os arquivos SQLs em assets.


#### Para subir o back-end localmente faremos os seguintes comandos:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Para subir o front-end localmente faremos os seguintes comandos em outro terminal:
```bash
cd frons/aila
npm i
npm run dev
```


### Como demonstrar
Após realizar a instalação e configuração. Acesse a aplicação em http://localhost:5173 para utilizar o frontend e http://localhost:8000/docs para visualizar os endpoints do backend.

Logins:

Agência - Senha

1 - 12345678

2 - 12345678

3 - 12345678

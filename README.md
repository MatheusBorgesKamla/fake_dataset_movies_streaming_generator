
# Movies Streaming Dataset Generator

Repositório com o intuito de armazenar os entregáveis do primeiro desafio proposto no bootcamp de engenharia de dados da How Education. O desafio consistia de criar um dataset utilizando a biblioteca [Faker](https://faker.readthedocs.io/en/master/) do Python e depois criar um pipeline com o intuito de realizar a ingestão na AWS, armazenando o dado no S3 e depois disponibilizando para consulta no Athena.

Ou seja, as seguintes etapas deveriam ser realizadas:

- Criar uma conta AWS
- Gerar dados necessários utilizando a biblioteca [Faker](https://faker.readthedocs.io/en/master/) do Python
- Realizar ingestão em um Bucket do AWS S3
- Criar um Crawler pelo AWS Glue para disponibilizar dados no AWS Athena
- Escrever exemplos de consultas nos dados utilizando o AWS Athena


## Projeto proposto
Para resolução do desafio foi proposto o cenário de um aplicativo de streaming de files e series, sendo gerado dois datasets:

- `users_dataset.csv` : Dataset de usuários cadastrados na plataforma com as seguintes informações

| coluna     | descrição |
|------------|-----------|
| account_id |id único do usuário|
| gender     |genêro (M ou F)|
| first_name |primeiro nome|
| last_name  |sobrenome|
| full_name |nome completo|
| email| e-mail de cadastro|
| address_city| cidade|
| address_state | estado|
| address_number| número da rua/endereço|
| address_street| nome da rua|
| post_code| código postal (cep)|
| birthday| data de nascimento|
| registration_date| data de registro na plataforma|
| churn_date| data de churn (inativação) na plataforma|
| contracted_plan| plano contratado (Basic, Intermediary ou Premium)|

- `movies_events.json` : Dataset com eventos de filmes acessados/assitidos por cada usuário

| coluna     | descrição |
|------------|-----------|
| id |id do filme|
| name     |nome do filme|
| img_url |endereço (url) para poster do filme|
| caption  |legenda do filme|
| genre | gênero do filme|
| type| se é um filme mesmo ou uma série|
| movie_release_date| data de lançamento do filme|
| datetime | timestamp de quando o filme foi acessado|
| has_fished| se o usuário finalizou o filme|
| account_id| id único do usuário|



## Pipeline Desenvolvido

![Alt Text](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/files/pipeline.png)


## Arquivos

O script **[lib/users_generator.py](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/libs/users_generator.py)** armeza as seguintes classes:
- `User`: Classe responsável por gerar dado de um único usuário a partir da lib Faker
- `Users_Generator`: Classe responsável por gerar um conjunto de Users e gerar csv


O script **[lib/movies_database_generator.py](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/libs/movies_database_generator.py)** armeza as seguintes classes:
- `Movie`: Classe responsável por requisitar dados da Rapid API trazendo informações de um filme aleatório
- `Movies_Events_Generator`: Classe responsável por gerar um conjunto de dados de eventos de usuários que acessaram cada filme


O script **[lib/writing.py](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/libs/writing.py)** armeza as seguintes classes:
- `Writer`: Classe auxiliar responsável por escrita dos datasets


Script **[main.py](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/main.py)** armezana função main responsável por instanciar as classes e chamar métodos para escrever os datasets

Script **[aws_ingest.py](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/aws_ingest.py)** é responsável por gerar bucket na AWS S3 e fazer a ingestão dos datasets

## AWS S3
Os datasets foram ingeridos no S3 utilizando a lib **boto3**, sendo criado um bucket ${AWS::AccountId}-landing-zone. Para cada dataset foi criado uma folder com o seguinte path:
- users/users_dataset.csv
- movies_events/movies_events_dataset.json

![Alt Text](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/files/s3_pic1.png)
![Alt Text](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/files/s3_pic2.png)
![Alt Text](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/files/s3_pic3.png)




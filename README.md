
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

| coluna     | descricao |
|------------|-----------|
| account_id |           |
| gender     |           |
| first_name |           |
| last_name  |           |
| full_name |           |
| first_name|           |
| email|           |
| address_city |           |
| first_name |           |



## Pipeline Desenvolvido

![Alt Text](https://github.com/MatheusBorgesKamla/fake_dataset_movies_streaming_generator/blob/main/files/pipeline.png)


## Arquivos
- O script lib/users_generator.py é responsável por gerar o dataset .csv de usuários cadastrados` 

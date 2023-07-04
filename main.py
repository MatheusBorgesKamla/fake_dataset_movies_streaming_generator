from libs.users_generator import Users_Generator
from libs.movies_database_generator import Movies_Events_Generator
import datetime
from dotenv import load_dotenv
from os import getenv
from faker import Faker

if __name__ == "__main__":
    load_dotenv("/home/matheus/.env")
    generator_users = Users_Generator(locate="pt_BR", sample_quantity=5000, start_date = datetime.date(2020, 1, 1), seed=18)
    generator_users.run()
    print("Users account database writed with sucess!")
    generator_users.save_csv("users_dataset.csv", overwrite=True)

    generator_movies = Movies_Events_Generator(generator_users.return_data(), 5000, datetime.date(2020, 1, 1), getenv("MOVIE_API_KEY"))
    generator_movies.run(overwrite=False)


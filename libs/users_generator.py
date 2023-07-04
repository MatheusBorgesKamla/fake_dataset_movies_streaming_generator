from faker import Faker
import numpy as np
import datetime
import math
from libs.writing import Writer


class User:
    #Classe responsável por gerar dados de um usuário
    def __init__(self, fake: Faker, start_date: datetime.date) -> None:
        #ID único do usuário
        self.account_id = fake.unique.random_number()
        #Dados usuário
        self.gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        self.first_name = fake.first_name_male() if self.gender == "M" else fake.first_name_female()
        self.last_name = fake.last_name()
        self.email = f"{self.first_name.lower().replace(' ','')}_{self.last_name.lower()}@{fake.domain_name()}"
        #Dados de endereço
        self.address_city = fake.city()
        self.address_state = fake.state_abbr()
        self.country = fake.current_country()
        self.address_number = fake.building_number()
        self.address_street = fake.street_name()
        self.post_code = fake.postcode()
        #Data de nasc, registro e saída da plataforma
        self.birthday = fake.date_of_birth(minimum_age=18, maximum_age=90)
        self.registration_date = fake.date_between_dates(date_start=start_date)
        
        is_churn = np.random.choice([True,False], p=[0.3,0.7])

        if is_churn and self.registration_date <= (datetime.date.today() - datetime.timedelta(days=30)):
            self.churn_date = fake.date_between_dates(date_start=(self.registration_date + datetime.timedelta(days=30)))
        else:
            self.churn_date = None
        
        self.contracted_plan = np.random.choice(["Basic","Intermediary","Premium"], p=[0.5,0.3,0.2])
    #Retorna nome completo
    @property
    def full_name(self) -> str:
        #Gera nome completo
        return self.first_name + " " + self.last_name
    #Retorna descrição completa do endereço
    @property
    def address_description(self) -> str:
        #Gera descrição completa do endereço
        return f"{self.address_street} - {self.address_number} | {self.post_code} | {self.address_city} - {self.address_state}, {self.country}"
    #Retorna idade atual do usuário
    @property
    def age(self) -> int:
        #Calcula idade
        return math.floor((datetime.date.today() - self.birthday).days / 365.2425)
    #Retorna dados do usuário como um dicionário do python
    def return_dict(self) -> dict:
        aux_dict = {
            "account_id":self.account_id,
            "gender":self.gender,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "full_name":self.full_name,
            "email":self.email,
            "address_city":self.address_city,
            "address_state":self.address_state,
            "country":self.country,
            "address_number":self.address_number,
            "address_street":self.address_street,
            "post_code":self.post_code,
            "birthday":self.birthday.strftime('%Y-%m-%d'),
            "registration_date":self.registration_date.strftime('%Y-%m-%d'),
            "churn_date":self.churn_date.strftime('%Y-%m-%d') if self.churn_date else None,
            "contracted_plan":self.contracted_plan
        }

        return aux_dict
    #Reescreve método print da classe
    def __str__(self) -> str:
        print_expr_1 = f"Gender: {self.gender}\nName: {self.full_name}\nE-mail: {self.email}\nAddress: {self.address_description}\nBirthday: {self.birthday}\nAge: {self.age}"
        print_expr_2 = f"Registration Date: {self.registration_date}\nChurn Date: {self.churn_date}\nContracted Plan: {self.contracted_plan}"
        return f"-----------------\nAccount ID: {self.account_id}\n" + print_expr_1 + "\n" + print_expr_2 + "\n-----------------"


class Users_Generator:
    #Classe responsável por gerar dataset de usuários
    def __init__(self, locate: str, sample_quantity: int, start_date: datetime.date, seed=None) -> None:
        self.locate = locate
        self.seed = seed
        self.sample_quantity = sample_quantity

        self._faker = Faker(self.locate)
        self._users_list = []
        self.start_date = start_date

        if self.seed:
            Faker.seed(self.seed)
    #Método responsável por gerar de fato os dados
    def run(self, verbose = False) -> list:
        for i in range(self.sample_quantity):
            user = User(self._faker, self.start_date)
            
            if verbose:
                print(f"Generating User {i+1}º")
                print(user)
            
            self._users_list.append(user)
        return self._users_list
    #Retorna IDs dos usuários gerados como uma lista
    def return_ids(self) -> list:
        ids_list = []
        
        if len(self._users_list) == 0:
            print("Empty data. Call method .run() first")
        else:
            for user in self._users_list:
                ids_list.append(user.account_id)
        
        return ids_list
    #Retorna os dados de usuários gerado como uma lista de Users
    def return_data(self) -> list:
        return self._users_list
    #Retorna os dados de usuários gerado como uma lista de dicionário
    def return_data_dict(self) -> list:
        data = []

        if len(self._users_list) == 0:
            print("Empty data. Call method .run() first")
        else:
            for user in self._users_list:
                data.append(user.return_dict())
        
        return data
    #Salva dados em csv
    def save_csv(self, path: str, overwrite:bool) -> None:
        data = self.return_data_dict()
        writer = Writer(path)
        writer.write_csv(data)
        
    
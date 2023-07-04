import requests
import datetime
from faker import Faker
import logging
import numpy as np
import ratelimit
from backoff import on_exception, expo
from libs.writing import Writer
import json

class Movie:

	def __init__(self, fake: Faker, start_date: datetime.date, api_key: str, user_register_date: datetime.date, user_churn_date = None, type = "Movies") -> None:
		self._fake = fake
		self.start_date = start_date
		self.user_register_date = user_register_date
		self.user_churn_date = user_churn_date
		self.type = type
		if type not in ["Movies","Series"]:
				logging.error("type parameter must be 'Movies' or 'Series'")
		else:
				self._type_list = "most_pop_movies" if type == "Movies" else "most_pop_series"
		
		self._api_url = "https://moviesdatabase.p.rapidapi.com/titles/random"

		self._api_param = {"list":self._type_list, "year":self.year, "limit":"10", "genre":self.genre}
		
		self._api_headers = {
			"X-RapidAPI-Key": api_key,
			"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
		}
		
		self._json_requested = self._request_movie()
		#print(self._json_requested)
		self.name = self._json_requested.get("originalTitleText").get("text")
		self.img_url = "" if self._json_requested.get("primaryImage") is None else self._json_requested.get("primaryImage").get("url")
		self.id = self._json_requested.get("id")
		self.caption = "" if self._json_requested.get("primaryImage") is None else self._json_requested.get("primaryImage").get("caption").get("plainText")

		if self._json_requested.get("releaseDate") is None:
			self.release_date = datetime.date(1666,1,1)
		else:
			self.release_date = datetime.date(year=int(1666 if self._json_requested["releaseDate"]["year"] == None else self._json_requested["releaseDate"]["year"]), 
											  month=int(1 if self._json_requested["releaseDate"]["month"] == None else self._json_requested["releaseDate"]["month"]),
											  day=int(1 if self._json_requested["releaseDate"]["day"] == None else self._json_requested["releaseDate"]["month"])
											)

	@property
	def year(self) -> str:
		year = self._fake.date_between_dates(date_start=self.start_date).year
		return str(year)
	
	@property
	def genre(self) -> str:
		genre_list = [
			"Action",
			"Adventure",
			"Animation",
			"Biography",
			"Comedy",
			"Crime",
			"Documentary",
			"Drama",
			"Family",
			"Fantasy",
			"Film-Noir",
			"Game-Show",
			"History",
			"Horror",
			"Music",
			"Mystery",
			"News",
			"Reality-TV",
			"Romance",
			"Sci-Fi",
			"Short",
			"Sport",
			"Thriller",
			"War",
			"Western"]
		return np.random.choice(genre_list)
	
	@property
	def has_finished(self) -> str:
		return np.random.choice(["True","False"],p=[0.6, 0.4])
	
	@property
	def date_time(self) -> datetime.datetime:
		if self.user_churn_date is None:
			aux = self._fake.date_time_between(start_date=self.user_register_date)
		else:
			aux = self._fake.date_time_between(start_date=self.user_register_date, end_date=self.user_churn_date)
		return aux
		
	@on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
	@ratelimit.limits(calls=29, period=30)
	@on_exception(expo, requests.exceptions.HTTPError, max_tries=10)

	def _request_movie(self) -> dict:
		response = requests.get(self._api_url, headers=self._api_headers, params=self._api_param, timeout=5)
		response.raise_for_status()
		response = response.json()["results"]
		
		if len(response) > 0:
			return response[0]
		else:
			return {"originalTitleText":{"text":"SYSTEM_ERROR_404"},
	   				"primaryImage":{"url":"SYSTEM_ERROR_404", "caption":{"plainText":"SYSTEM_ERROR_404"}},
					"id":"SYSTEM_ERROR_404",
					"releaseDate":{"year":"1666","month":"1","day":"1"}
	   				}
	
	def return_dict(self) -> dict:
		aux_dict = {
            "id":self.id,
            "name":self.name,
            "img_url":self.img_url,
            "caption":self.caption,
            "genre":self.genre,
	        "type":self.type,
            "movie_release_date":self.release_date.strftime('%Y-%m-%d'),
			"datetime":self.date_time.strftime('%Y-%m-%d %H: %M: %S'),
	    	"has_fished":self.has_finished
        }
		 
		return aux_dict
	

class Movies_Events_Generator:
	def __init__(self, users_account_list: list, sample_quantity: int, start_date: datetime.date, api_key: str) -> None:
		self.users_list = users_account_list

		self.sample_quantity = sample_quantity

		self.start_date = start_date

		self._api_key = api_key

		self._faker = Faker()

		self._data = []
	
	
	def run(self, save_file = True, overwrite = True) -> None:
		i = 0
		writer = Writer("movies_events.json")

		if overwrite:
			writer.erase_file()

		while i < self.sample_quantity:
			max = len(self.users_list) - 1

			index = np.random.randint(low=0, high=max)

			user = self.users_list[index]

			movie = Movie(self._faker, self.start_date, self._api_key, user.registration_date, user.churn_date, np.random.choice(["Movies","Series"]))

			if movie.name != "SYSTEM_ERROR_404":
				i = i + 1
				final_dict = movie.return_dict()
				final_dict["account_id"] = user.account_id
				self._data.append(final_dict)
				writer.write_row(json.dumps(final_dict))
				print(f"Requesting and writing {i}/{self.sample_quantity} movie event ....")
	
	def return_data(self) -> list:
		return self._data



				
    
        
        
    

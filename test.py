# -*- coding: utf-8 -*-
import difflib
from flask import Flask, request, g, render_template, url_for, redirect, flash, make_response, session,jsonify,abort, send_from_directory
from flask_restful import Api, Resource, reqparse


application = Flask(__name__, template_folder="app/templates",static_folder="app/static",static_url_path='')
application.config['JSON_AS_ASCII'] = False
application.jinja_env.filters['is_int'] = lambda u: u if type(u) is int else f'{u[0]}|{u[1]}'

class NumberWeek(object):
	
	WEEK_N = 1 # Номер недели
	
	MONTH = {
		'январь':('january',1,31,0),
		'февраль':('february',1,(28,29),1),
		'март':('march',2,31,2),
		'апрель':('april',2,30,3),
		'май':('may',2,31,4),
		'июнь':('june',3,30,5),
		'июль':('july',3,31,6),
		'август':('august',3,30,7),
		'сентябрь':('september',4,30,8),
		'октябрь':('october',4,31,9),
		'ноябрь':('november',4,30,10),
		'декабрь':('december',1,31,11)
	}
	
	SESONE = ['Зима','Весна','Лето','Зима']
	
	def __init__(self,day=1,month=1,year=2019,console=True):
		self.year = year if year >= 2019 else 2019
		p = int(self.is_visok())
		try:
			if type(month) is int:
				if month < 1:
					while month <= -12:
						month = month+12
					month = 12 if month == 0 else month
					month = month if month > 0 else -1*month
				elif month > 12:
					while month >= 12:
						month = month-12
					month = 1 if month == 13 else month
				month = list(self.MONTH.items())[month-1][1]
			elif type(month) is str:
				if month.lower() in list(self.MONTH.keys()):
					month = self.MONTH[month.lower()]
				else:
					del_len = [len(i) for i in list(self.MONTH.keys())]
					k = sum(del_len)/len(del_len)
					for i in list(self.MONTH.keys()):
						rat = difflib.SequenceMatcher(None,month.lower(),i).ratio()
						if rat >= (len(month.lower())/k):
							month = self.MONTH[i]
							break
					else:
						raise BaseException('Месяц не найден')
			if type(month[2]) is int:
				if not ((day>0) and (day<=month[2])):
					raise BaseException('День введен не верно')
			elif type(month[2]) is tuple:
				if not ((day>0) and (day<=month[2][p])):
					raise BaseException('День введен не верно')
			des = [i[2] if not type(i[2]) is tuple else i[2][p] for i in list(self.MONTH.values())]
			delt_day = (sum(des)*month[3])//(len(des)*7)
			self.WEEK_N = ((day//7)+1)+(delt_day)
			self.day = day
			self.month = month
			if console:
				print(f'{self.SESONE[month[1]-1]}, {day} {month[0].title()} {year} год')
		except BaseException as e:
			raise e

	def get_sesone(self): # Выдает текущий сезон года
		return self.SESONE[self.month[1]-1]

	def is_visok(self): # Определяет какой год високосный или нет
		return True if ((self.year%4==0 and self.year%100!=0) or self.year%400==0 ) else False

@application.route("/")
def index():
	day = request.args.get('day',default=1,type=int)
	month = request.args.get('month',default=1,type=int)
	year = request.args.get('year',default=2019,type=int)
	nw = NumberWeek(day,month,year,False)
	return render_template(
		"index.html",
		title = 'Тестовое задание',
		NW = nw.WEEK_N,
		MaxDays = nw.month[2][int(nw.is_visok())] if type(nw.month[2]) is tuple else nw.month[2],
		day = day,
		month = month,
		year = year,
		months = nw.MONTH
	),200

if __name__ == '__main__':
	application.run(host="127.0.0.1",port=5000,debug=True)

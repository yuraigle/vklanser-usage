# coding=utf-8
import os, datetime
from vklancer import api
from vklancer import utils

cwd = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cwd, 'auth.txt')) as file:
    lines = [line.rstrip('\n') for line in file]

access_token = utils.oauth(lines[0], lines[1])
vk = api.API(token=access_token, version='5.37')
home = os.path.expanduser("~")
out1 = os.path.join(home, 'Desktop', 'users.csv')
f1 = open(out1, 'a')

groups_in = [118445684]
already_in = []
for gr in groups_in:
	age = 18
	while age < 22:
		response = vk.users.search(count=1000, offset=0, city=57, country=1, 
			sex=1, age_from=age, age_to=age, group_id=gr, 
			fields='sex, screen_name, last_seen, relation')
		for usr in response['response']['items']:
			skip = False

			# уже есть в списке
			if usr['id'] in already_in:
				skip = True

			# нет онлайн неделю
			seen = datetime.datetime.fromtimestamp(usr['last_seen']['time'])
			if seen < datetime.datetime.today() - datetime.timedelta(days=7):
				skip = True

			if not skip:
				f1.write(str(usr['id']) + '\t')
				f1.write(usr['last_name'].encode('utf8') + '\t')
				f1.write(usr['first_name'].encode('utf8') + '\t')
				f1.write('https://vk.com/' + usr['screen_name'].encode('utf8') + '\t')
				if usr.has_key('relation'):
					f1.write(str(usr['relation']))
				f1.write('\t')
				f1.write(str(age) + '\n')
				already_in.append(usr['id'])
		age += 1
		print(str(gr) + ' ' + str(age))

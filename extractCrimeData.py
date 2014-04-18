import csv
import datetime
import pickle

def main(crimeFile, beatFile):
	csvfile = open(crimeFile, "rB")
	reader = csv.reader(csvfile)
	crimes = []
	beats = {}
	violentCrimes = ['CRIM SEXUAL ASSAULT', 'OFFENSE INVOLVING CHILDREN', 'BATTERY', 'ROBBERY', 'HOMICIDE', 'ASSAULT', 'SEX OFFENSE', 'PUBLIC PEACE VIOLATION', 'ARSON', 'WEAPONS VIOLATION', 'KIDNAPPING', 'STALKING', 'INTIMIDATION']

	for row in reader:
		if row[5] in violentCrimes:
			crimes.append(row)

	for crime in crimes[1:]:
		beat = crime[10]
		if beat not in beats:
				beats[beat] = {}
				beats[beat]['crimes'] = {'2/28':[], '3/1':[], '3/2':[], '3/3':[], '3/4':[], '3/5':[], '3/6':[], '3/7':[], '3/8':[], '3/9':[], '3/10':[], '3/11':[], '3/12':[], '3/13':[], '3/14':[]}
				beats[beat]['tweets'] = []
				beats[beat]['features'] = []
		date = datetime.datetime.strptime(crime[2], "%m/%d/%Y %H:%M:%S %p")
		key = str(date.month) + "/" + str(date.day)
		beats[beat]['crimes'][key].append(crime)

	pickle.dump(beats, open(beatFile, "wb"))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
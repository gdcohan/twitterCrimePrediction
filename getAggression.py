import os
import sqlite3 as lite
import csv
import pickle

def main(beatFile, outcomesFile, featuresFile):
	beats = pickle.load(open(beatFile, "rB"))
	DBDayMap = {"2/28": "day1Tweets.db", "3/1":"day2Tweets.db", "3/2":"day3Tweets.db", "3/3":"day4Tweets.db", "3/4":"day5Tweets.db", "3/5":"day6Tweets.db", "3/6":"day7Tweets.db", "3/7":"day8Tweets.db","3/8":"day9Tweets.db","3/9":"day10Tweets.db", "3/10" : "day11Tweets.db", "3/11" : "day12Tweets.db", "3/12" : "day13Tweets.db", "3/13" : "day14Tweets.db", "3/14" : "day15Tweets.db"}
	print("loaded Beat file")
	features = []
	outcomes = []
	for beat in beats:
		days = beats[beat]
		for day in days:
			featureArray = []
			outcome = getOutcomeVariable(beats[beat][day]['crimes'])
			outcomes.append(outcome)
			getDBFeatures(featureArray, beats[beat][day]['tweets'], "aggresive", "aggressive", DBDayMap[day], 'non-aggressive')
			features.append(featureArray)
			beats[beat][day]['features'] = [outcome] + featureArray
			print("Done with " + day + " in beat: " + beat + ". Its features were: ")
			print(featureArray)
			print(" and it's outcome was: " + str(outcome))
		print("Done with beat: " + beat)
	pickle.dump(outcomes, open(outcomesFile, "wB"))
	print("dumped outcomes")
	pickle.dump(features, open(featuresFile, "wB"))
	print("dumped features")
	pickle.dump(beats, open("finalBeats.p", "wB"))

def getOutcomeVariable(crimeArray):
	if len(crimeArray) > 0:
		return 1
	else:
		return 0

def getDBFeatures(featArray, tweetArray, dbField, dbValue, dbFilename, alternativeOutcome):
	con = lite.connect("DBs/" + dbFilename)
	cur = con.cursor()
	count = 0
	total = 0
	for tweet in tweetArray:
		tweetID = tweet[0]
		cur.execute("Select {0} from TweetData where id = {1};".format(dbField, tweetID))
		tweetEntry = cur.fetchone()
		if tweetEntry[0] == dbValue:
			count += 1
			total += 1
		elif tweetEntry[0] == alternativeOutcome:
			total += 1
	if total > 0:
		featArray.append(float(count) / total * 100)
	else:
		featArray.append(0)
	featArray.append(count)

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3])

import csv
import sqlite3 as lite
import os

def main():
	aggressionFilenames = os.listdir("aggressionPredictions")
	aggressionFilenames.sort()
	dbFilenames = os.listdir("DBs")
	dbFilenames.sort()
	for i in range(len(aggressionFilenames)): 
		con = lite.connect("DBs/" + dbFilenames[i])
		cur = con.cursor()
		putAggressionRatingIntoDB(con, cur, "aggressionPredictions/" + aggressionFilenames[i], "aggresive")
		print("done with: " + aggressionFilenames[i])
		con.close()

def putAggressionRatingIntoDB(con, cur, filename, fieldname):
	csvfile = open(filename, "rB")
	reader = csv.reader(csvfile, delimiter = '\t')
	rows = []
	count = 0
	for row in reader:
		rows.append(row)
	for row in rows[1:]:
		count += 1
		if count % 1000 == 0: 
			print("updated tweet num: " + str(count))
		rating = row[2]
		text = row[5]
		cur.execute("UPDATE TweetData SET '{0}' = '{1}' where tweet = '{2}';".format(fieldname, rating, text))
	con.commit()

if __name__ == '__main__':
	main()

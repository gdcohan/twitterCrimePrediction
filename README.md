twitterCrimePrediction
======================

Using Twitter to Predict Crime:

Python Libraries:
scikit-learn
sqlite3
shapefile

Steps for replicating thesis:

1) Add tweets2.db back into tweets.db
2) run "python extractCrimeData.py Crimes_-_2001_to_present.csv crimes.p"
3) run "python tweetsForBeats.py crimes.p tweets.db geo_aerh-rz74-1.shp beats.p"
4) divide tweets.db into different db for each day, put them in directory named "DBs"
5) run "python putRatingsInDb.py"
6) run "python getAggression.py beats.p outcomes.p features.p"
7) run "python cross_validate.py [NUM_FOLDS] features.p outcomes.p"
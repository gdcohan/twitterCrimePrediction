twitterCrimePrediction
======================

Using Twitter to Predict Crime:

Python Libraries:
scikit-learn
sqlite3
shapefile

Steps for replicating thesis:

1) Add tweets2.db back into tweets.db 
2) run "python extractCrimeData.py Crimes_-_2001_to_present.csv [OUTPUT_FILE_NAME]"
3) run "python tweetsForBeats.py [OUTPUT_FILE_NAME] tweets.db geo_aerh-rz74-1.shp [OUTPUT2_FILE_NAME]"
4)

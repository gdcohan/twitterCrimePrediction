from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
import random
import math
import pickle

def main(numFolds, features, outcomes):
	fDict = pickle.load(open(features, "rb"))
    oDict = pickle.load(open(outcomes, "rb"))
    
    feats = fDict['train'] + fDict['cv'] + fDict['test']
    outcomes = oDict['train'] + oDict['cv'] + oDict['test']

	twitterFeats = []
	historyFeats = []
	for i in range(len(feats)):
		twitterFeats.append(feats[i][:-1])
		historyFeats.append([feats[i][-1]])
	print("All data:")
	crossValidate(feats, outcomes, numFolds)
	print("Twitter data:")
	crossValidate(twitterFeats, outcomes, numFolds)
	print("Historical data:")
	crossValidate(historyFeats, outcomes, numFolds)

def crossValidate(feats, outcomes, numFolds):
	scaler = StandardScaler()
	featureFolds, outcomeFolds = generateFolds(feats, outcomes, numFolds)
	avgSGD = 0
	avgSVM = 0
	avgRFC = 0
	for i in range(numFolds):
		trainFeats, testFeats, trainOutcomes, testOutcomes = generateData(featureFolds, outcomeFolds, i)
		scaler = scaler.fit(trainFeats)
		scaledTrainFeats = scaler.transform(trainFeats)
		scaledTestFeats = scaler.transform(testFeats)
		clf = SGDClassifier(n_iter=400, shuffle=True, loss='hinge', penalty='l1')
		clf.fit(scaledTrainFeats, trainOutcomes)
		avgSGD += clf.score(scaledTestFeats, testOutcomes)

		clf = svm.SVC(C=0.5)
		clf.fit(scaledTrainFeats, trainOutcomes)
		avgSVM += clf.score(scaledTestFeats, testOutcomes)

		clf = RandomForestClassifier(n_estimators=100)
		clf.fit(trainFeats, trainOutcomes)
		avgRFC += clf.score(testFeats, testOutcomes)

	print("SGD: " + str(avgSGD / float(numFolds)))
	print("SVM: " + str(avgSVM / float(numFolds)))
	print("RFC: " + str(avgRFC / float(numFolds)))


def generateFolds(feats, outcomes, numFolds):
	randomOrder = range(len(feats))
	random.shuffle(randomOrder)
	feats = [feats[i] for i in randomOrder]
	outcomes = [outcomes[i] for i in randomOrder]
	chunkLength = int(math.floor(len(feats) / float(numFolds)))
	featureFolds = []
	outcomeFolds = []
	for i in range(0, len(feats), chunkLength):
		featureFolds.append(feats[i:i+chunkLength])
		outcomeFolds.append(outcomes[i:i+chunkLength])
	return featureFolds, outcomeFolds

def generateData(featFolds, outcomeFolds, numFold):
	trainFeats = []
	trainOutcomes = []
	testFeats = []
	testOutcomes = []
	for i in range(len(featFolds)):
		if i == numFold:
			testFeats = featFolds[i]
			testOutcomes = outcomeFolds[i]
		else:
			trainFeats += featFolds[i]
			trainOutcomes += outcomeFolds[i]
	return trainFeats, testFeats, trainOutcomes, testOutcomes

if __name__ == '__main__':
	main(sys.argv[1], sys.agrv[2], sys.argv[3])
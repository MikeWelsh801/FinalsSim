#!/bin/bash

NN_FOLDER="./NN Stuff/"
TRAIN_DATA_FILE="$NN_FOLDER"NBA_Training_Data_"$3".csv
HOME_PREDICT="$NN_FOLDER""$1"_at_home_prediction_"$3".csv
AWAY_PREDICT="$NN_FOLDER""$2"_at_home_prediction_"$3".csv
TRAIN_PROBS_FILE="$NN_FOLDER"train_"$1"_"$2"_"$3".txt

# look for and generate training data
echo "Looking for $TRAIN_DATA_FILE ..."

if [ ! -f "$TRAIN_DATA_FILE" ]; then
    echo "Training data file not yet generated for $3."
    echo "Creating data..."
    python bbscrape.py $3 
    echo "$TRAIN_DATA_FILE created."
else
    echo "Training data file found."
fi

# look for prediction files and generate
echo "Looking for $HOME_PREDICT and $AWAY_PREDICT ..."

if [[ ! -f "$HOME_PREDICT"  ||  ! -f "$AWAY_PREDICT" ]]; then
    echo "Prediction files not found for home team: $1, away team: $2, year: $3"
    echo "Creating data..."
    python bbscrape.py -p "$1" "$2" "$3"
    echo "$HOME_PREDICT and $AWAY_PREDICT created."
else
    echo "Prediction files found."
fi

# look for trained file
echo "Looking for $TRAIN_PROBS_FILE ..."

if [ ! -f "$TRAIN_PROBS_FILE" ]; then
    ./train.sh "$1" "$2" "$3"
    echo "Neural Network trained. Probalitities generated."
else
    echo "Neural Network already trained."
fi

./model.sh "$TRAIN_PROBS_FILE"

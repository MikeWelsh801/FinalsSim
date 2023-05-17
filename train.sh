#!/bin/bash/

# this trains and evaluates the example inputs
# it only saves the output probabilities
NN_FOLDER="./NN Stuff/"
echo Training network and getting probabilities...

echo "home team: $1"
echo "away team: $2"
echo "year: $3"
python NeuralNet.py "$1" "$2" "$3" > "$NN_FOLDER"train_"$1"_"$2"_"$3".txt

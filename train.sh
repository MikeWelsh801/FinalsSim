#!/bin/bash/

# this trains and evaluates the example inputs
# it only saves the output probabilities
echo Training network and getting probabilities...

echo "home team: $1"
echo "away team: $2"
echo "year: $3"
python NeuralNet.py "$1" "$2" "$3" > train.txt

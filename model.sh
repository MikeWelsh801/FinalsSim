#!/bin/bash

# Runs the sim with the trained output probabilities.
train_path=../../../../
exec_path=./FinalsSim/bin/Debug/net6.0

echo entering $exec_path...
cd $exec_path

echo running sim...

./FinalsSim $train_path"$1"

echo leaving $exec_path
cd $train_path


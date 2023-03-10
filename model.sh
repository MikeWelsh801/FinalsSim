train_path=../../../../
exec_path=./FinalsSim/bin/Debug/net6.0

echo entering $exec_path ...
cd $exec_path

echo running sim ...

./FinalsSim $(cat $train_path/train.txt)

echo leaving $exec_path
cd $train_path


train_path=../../../../
exec_path=./FinalsSim/bin/Debug/net6.0

cd $exec_path

./FinalsSim $(cat $train_path/train.txt)

cd $train_path


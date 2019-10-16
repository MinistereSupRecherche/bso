echo "model calibration"
 ./fasttext supervised -input pf_dataset.train  -output model_pf_20190304 -lr 0.05 -epoch 30 -wordNgrams 2 -dim 100 -loss hs -bucket 200000

echo "precision @1"
./fasttext test model_pf_20190304.bin pf_dataset.test

echo "precision @5"
./fasttext test model_pf_20190304.bin pf_dataset.test 5

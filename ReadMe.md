## Install the inviroment:
```bash
conda env create -f environment.yaml
```
## Download the raw data table files:
```bash
pip install gdown
gdown 1RhTU-xNuTBa-t7mCgyD6ZOpPYmsJnyDQ
tar -xvf adobe_train_gt.tar  
```

## Run the script to generate the dataset:
```bash
python -m chartcrafter.chart_pair_generator
```

The output dir would be in ./out/


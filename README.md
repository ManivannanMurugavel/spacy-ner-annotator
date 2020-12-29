# spacy-ner-annotator


## Installation
pip3 install spacy

## Steps for usage
1. Open `index.html` file and open data on it. 
2. Post annotations download the data and convert to spacy format using `convert_spacy_train_data.py`
3. Split data into train and test if you wish and add it to `train.py`
4. finally run the train.py after setting the hyper-parameters. Iterations are losses are logged in `output_log.txt`. And precision, recall and f1 scores are logged in `train_output.txt` and `test_output.txt`
5. Check progress by running `losses_plotter.py`.
6. If you wish to train over a model download the model and add its name in `train.py` 

## Details & Credits
Visit this url:

```
https://manivannanmurugavel.github.io/annotating-tool/spacy-ner-annotator/
```
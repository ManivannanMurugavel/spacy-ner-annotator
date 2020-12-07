import spacy
import random
import time
import warnings
from spacy.util import minibatch, compounding

# Settings for google Collab
# spacy.require_gpu()
# gpu = spacy.prefer_gpu()
# print('GPU:', gpu)


# Downloading models
# spacy.cli.download("en_core_web_sm")
# spacy.cli.download("en_core_web_lg")


TRAIN_DATA = [('what is the price of polo?', {'entities': [(21, 25, 'PrdName')]}), ('what is the price of ball?', {'entities': [(21, 25, 'PrdName')]}), ('what is the price of jegging?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of t-shirt?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of jeans?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of bat?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of shirt?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of bag?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of cup?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of jug?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of plate?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of glass?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of moniter?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of desktop?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of bottle?', {'entities': [(21, 27, 'PrdName')]}), ('what is the price of mouse?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of keyboad?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of chair?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of table?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of watch?', {'entities': [(21, 26, 'PrdName')]})]
random.seed(0)

file = open('output_log.txt','w') 
file.write("iteration_no" + "," + "losses" +"\n")

model = None # ("en_core_web_sm")   # Replace with model you want to train
start_training_time = time.time()

def train_spacy(data,iterations):

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    TRAIN_DATA = data

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    if model is None:
        optimizer = nlp.begin_training()

    else:
        print ("resuming")
        optimizer = nlp.resume_training()
        print (optimizer.learn_rate)
    
    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        for itn in range(iterations):
            
            file = open('outputlog.txt','a') # For logging losses of iterations 
            
            start = time.time() # Iteration Time
            
            if(itn%1200 == 0):
                print("Time Elapsed", time.time()-start_training_time)
                optimizer.learn_rate = 0.0001 # Lowering learning rate with iterations

            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}

            # use either batches or entire set at once

            ##### For training in Batches
            # sizes = compounding(1.0, 4.0, 1.001)
            # batches = minibatch(TRAIN_DATA, size=sizes)
            # for batch in batches:
            #     texts, annotations = zip(*batch)
            #     nlp.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)

            ###########################################

            ##### For training in as a single iteration
            
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)


            print("Losses",losses)
            file.write(str(itn) + "," + str(losses['ner']) +"\n")
            print ("time for iteration:", time.time()-start)
            file.close()

    return nlp


prdnlp = train_spacy(TRAIN_DATA, 20)

# Save our trained Model
modelfile = input("Enter your Model Name: ")
prdnlp.to_disk(modelfile)

#Test your text
test_text = input("Enter your testing text: ")
doc = prdnlp(test_text)
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
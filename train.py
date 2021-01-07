import spacy
import random
import time
import warnings
from spacy.util import minibatch, compounding, decaying
from spacy.gold import GoldParse
from spacy.scorer import Scorer


# Settings for google Collab
# spacy.require_gpu()
# gpu = spacy.prefer_gpu()
# print('GPU:', gpu)


# Downloading models
# spacy.cli.download("en_core_web_sm")
# spacy.cli.download("en_core_web_lg")


TRAIN_DATA = [('what is the price of polo?', {'entities': [(21, 25, 'PrdName')]}), ('what is the price of ball?', {'entities': [(21, 25, 'PrdName')]}), ('what is the price of jegging?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of t-shirt?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of jeans?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of bat?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of shirt?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of bag?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of cup?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of jug?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of plate?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of glass?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of moniter?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of desktop?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of bottle?', {'entities': [(21, 27, 'PrdName')]}), ('what is the price of mouse?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of keyboad?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of chair?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of table?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of watch?', {'entities': [(21, 26, 'PrdName')]})]

TEST_DATA =  [('what is the price of polo?', {'entities': [(21, 25, 'PrdName')]}), ('what is the price of ball?', {'entities': [(21, 25, 'PrdName')]}), ('what is the price of jegging?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of t-shirt?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of jeans?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of bat?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of shirt?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of bag?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of cup?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of jug?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of plate?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of glass?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of moniter?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of desktop?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of bottle?', {'entities': [(21, 27, 'PrdName')]}), ('what is the price of mouse?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of keyboad?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of chair?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of table?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of watch?', {'entities': [(21, 26, 'PrdName')]})]

random.seed(0)

# Log files for logging the train and testing scores for references
file = open('output_log.txt','w') 
file.write("iteration_no" + "," + "losses" +"\n")

file1 = open('test_output.txt','w')
file1.write("iteration_no"+ "," +"ents_p"+ "," +"ents_r"+ "," +"ents_f"+ "," +"ents_per_type"+ "\n")

file2 = open('train_output.txt','w')
file2.write("iteration_no"+ "," +"ents_p"+ "," +"ents_r"+ "," +"ents_f"+ "," +"ents_per_type"+ "\n")

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

        # For training with customized cfg 
        nlp.entity.cfg['conv_depth'] = 16
        nlp.entity.cfg['token_vector_width'] = 256
        # nlp.entity.cfg['bilstm_depth'] = 1
        # nlp.entity.cfg['beam_width'] = 2


    else:
        print ("resuming")
        optimizer = nlp.resume_training()
        print (optimizer.learn_rate)
    
    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    
    dropout = decaying(0.8, 0.2, 1e-6) #minimum, max, decay rate
    sizes = compounding(1.0, 4.0, 1.001)

    with nlp.disable_pipes(*other_pipes):  # only train NER
        
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        for itn in range(iterations):
            
            file = open('outputlog.txt','a') # For logging losses of iterations 
            
            start = time.time() # Iteration Time
            
            if(itn%100 == 0):
                print("Itn  : "+str(itn), time.time()-start_training_time)
                print('Testing')
               
                results = evaluate(nlp, TEST_DATA)
                file1 = open('test_output.txt','a') 
                file1.write(str(itn)+','+ str(results['ents_p'])+','+str(results['ents_r'])+','+str(results['ents_f'])+','+str(results["ents_per_type"])+"\n")
                file1.close()

                results = evaluate(nlp, TRAIN_DATA)
                file2 = open('train_output.txt','a') 
                file2.write(str(itn)+','+ str(results['ents_p'])+','+str(results['ents_r'])+','+str(results['ents_f'])+','+str(results["ents_per_type"])+"\n")
                file2.close()

                modelfile = "training_model"+str(itn)
                nlp.to_disk(modelfile)
  
            # Reducing Learning rate after certain operations 
            if (itn == 300):
                optimizer.learn_rate = 0.0001 
    
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}

            # use either batches or entire set at once

            ##### For training in Batches
            batches = minibatch(TRAIN_DATA, size=sizes)
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=next(dropout), losses=losses)

            ###########################################

            ##### For training in as a single iteration
            
            # for text, annotations in TRAIN_DATA:
            #     nlp.update(
            #         [text],  # batch of texts
            #         [annotations],  # batch of annotations
            #         drop=0.2,  # dropout - make it harder to memorise data
            #         # drop=next(dropout),  Incase you are using decaying drop
            #         sgd=optimizer,  # callable to update weights
            #         losses=losses)


            print("Losses",losses)
            file.write(str(itn) + "," + str(losses['ner']) +"\n")
            print ("time for iteration:", time.time()-start)
            file.close()

    return nlp


 
def evaluate(ner_model, test_data):
    scorer = Scorer()
    for input_, annot in test_data:
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot['entities'])
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    return scorer.scores




prdnlp = train_spacy(TRAIN_DATA, 500)

# Save our trained Model

# uncomment if you want to put model name through command line
# modelfile = input("Enter your Model Name: ")
modelfile = "Final_model"
prdnlp.to_disk(modelfile)

#Test your text
# test_text = input("Enter your testing text: ")
# doc = prdnlp(test_text)
# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)

# Prints Final -- f1 score, precision and recall
results = evaluate(prdnlp, TEST_DATA)
import json
print (json.dumps(results,indent=4))

import json

filename = input("Enter your train data filename(json) : ")
print(filename)


with open(filename) as train_data:
	train = json.load(train_data)

TRAIN_DATA = []
for data in train:
	ents = [tuple(entity[:3]) for entity in data['entities']]
	TRAIN_DATA.append((data['content'],{'entities':ents}))


with open('{}'.format(filename.replace('json','txt')),'w') as write:
	write.write(str(TRAIN_DATA))

print("[INFO] Stored the spacy training data and  filename is {}".format(filename.replace('json','txt')))
# print('-------------Copy and Paste to spacy training-------------')
# print()
# print()
# print()
# print(TRAIN_DATA)
# print()
# print()
# print()
# print('--------------------------End-----------------------------')

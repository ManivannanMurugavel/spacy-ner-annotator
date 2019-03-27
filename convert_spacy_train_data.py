import json

filename = input("Enter your train data filename : ")
print(filename)


with open(filename) as train_data:
	train = json.load(train_data)

TRAIN_DATA = []
for data in train:
	ents = [tuple(entity) for entity in data['entities']]
	TRAIN_DATA.append((data['content'],{'entities':ents}))


with open('{}'.format(filename.replace('json','txt')),'w') as write:
	write.write(str(TRAIN_DATA))

print('-------------Copy and Paste to spacy training-------------')
print()
print()
print()
print(TRAIN_DATA)
print()
print()
print()
print('--------------------------End-----------------------------')
import json
data= {"meta":{"title":"Computer Quiz","author":"Joshua Boag","length": 3},"questions":{"Q1":{"question":"How many Bits are in a Byte?","choices":["8 Bits","2 Bits","6 Bits","4 Bits"],"answer":1},"Q2":{"question":"Where many","choices":["1","2","three","4"],"answer":4},"Q3":{"question":"How much","choices":["one","2","3","4"],"answer":3}}}
with open('quiz.json', 'w') as fp:
    json.dump(data, fp,indent=4)

with open('quiz.json') as handle:
    dictdump = json.loads(handle.read())

print(dictdump)

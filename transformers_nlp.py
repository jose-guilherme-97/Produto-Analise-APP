from transformers import pipeline
from deep_translator import GoogleTranslator
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import pandas as pd

class NLP(object):
    def __init__(self, df):
        super(NLP, self).__init__()
        self.df = df
    
    def translate(self, initial_language = 'pt', final_language = 'en'):
        pipe = GoogleTranslator(source = initial_language, target = final_language)
        self.df["translated"] = self.df["content"].apply(lambda x: pipe.translate(x))
        return self.df
    
    def entity_recognition(self):
        model = "pierreguillou/ner-bert-large-cased-pt-lenerbr"
        ner_tag = pipeline('ner', aggregation_strategy = 'simple', model = model)
        reviews = self.df["content"].to_string(header=False, index=False).replace("\n",".")
        return pd.DataFrame(ner_tag(reviews))
    
    def question_answering(self, question):
        tokenizer = AutoTokenizer.from_pretrained("pierreguillou/bert-large-cased-squad-v1.1-portuguese")
        model = AutoModelForQuestionAnswering.from_pretrained("pierreguillou/bert-large-cased-squad-v1.1-portuguese")
        qa = pipeline('question-answering', model = model, tokenizer=tokenizer)
        reviews = self.df["content"].to_string(header=False, index=False).replace("\n",".")
        results = qa(question = question, context = reviews)
        return results["answer"]

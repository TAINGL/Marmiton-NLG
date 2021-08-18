import os
import io
import requests
import numpy as np
import pandas as pd
import re
import zipfile
import random
import time
import csv
import datetime
from itertools import compress
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from transformers import AutoTokenizer, AutoConfig, AutoModelForPreTraining, \
                         AdamW, get_linear_schedule_with_warmup, \
                         TrainingArguments, BeamScorer, Trainer

import torch
from torch.utils.data import Dataset, random_split, DataLoader, \
                             RandomSampler, SequentialSampler


SPECIAL_TOKENS  = { "bos_token": "<|BOS|>",
                    "eos_token": "<|EOS|>",
                    "unk_token": "<|UNK|>",                    
                    "pad_token": "<|PAD|>",
                    "sep_token": "<|SEP|>"}

MODEL           = 'antoiloui/belgpt2'

MAXLEN          = 768 

class myDataset(Dataset):

    def __init__(self, data, tokenizer, randomize=True):

        title, instruction, keywords = [], [], []
        for k, v in data.items():
            title.append(v[0])
            instruction.append(v[1])
            keywords.append(v[2])

        self.randomize = randomize
        self.tokenizer = tokenizer 
        self.title     = title
        self.instruction      = instruction
        self.keywords  = keywords  

    #---------------------------------------------#

    @staticmethod
    def join_keywords(keywords, randomize=True):
        N = len(keywords)

        #random sampling and shuffle
        if randomize: 
            M = random.choice(range(N+1))
            keywords = keywords[:M]
            random.shuffle(keywords)

        return ','.join(keywords)

    #---------------------------------------------#

    def __len__(self):
        return len(self.instruction)

    #---------------------------------------------#
    
    def __getitem__(self, i):
        keywords = self.keywords[i].copy()
        kw = self.join_keywords(keywords, self.randomize)
        
        input = SPECIAL_TOKENS['bos_token'] + self.title[i] + \
                SPECIAL_TOKENS['sep_token'] + kw + SPECIAL_TOKENS['sep_token'] + \
                self.instruction[i] + SPECIAL_TOKENS['eos_token']

        encodings_dict = tokenizer(input,                                   
                                   truncation=True, 
                                   max_length=MAXLEN, 
                                   padding="max_length")   
        
        input_ids = encodings_dict['input_ids']
        attention_mask = encodings_dict['attention_mask']
        
        return {'label': torch.tensor(input_ids),
                'input_ids': torch.tensor(input_ids), 
                'attention_mask': torch.tensor(attention_mask)}

def get_tokenier(special_tokens=None):
    tokenizer = AutoTokenizer.from_pretrained(MODEL) #GPT2Tokenizer

    if special_tokens:
        tokenizer.add_special_tokens(special_tokens)
        print("Special tokens added")
    return tokenizer

def get_model(tokenizer, special_tokens=None, load_model_path=None):

    #GPT2LMHeadModel
    if special_tokens:
        config = AutoConfig.from_pretrained(MODEL, 
                                            bos_token_id=tokenizer.bos_token_id,
                                            eos_token_id=tokenizer.eos_token_id,
                                            sep_token_id=tokenizer.sep_token_id,
                                            pad_token_id=tokenizer.pad_token_id,
                                            output_hidden_states=False)
    else: 
        config = AutoConfig.from_pretrained(MODEL,                                     
                                            pad_token_id=tokenizer.eos_token_id,
                                            output_hidden_states=False)    

    #----------------------------------------------------------------#
    model = AutoModelForPreTraining.from_pretrained(MODEL, config=config)

    if special_tokens:
        #Special tokens added, model needs to be resized accordingly
        model.resize_token_embeddings(len(tokenizer))

    if load_model_path:
        model.load_state_dict(torch.load(load_model_path, map_location ='cpu'))

    model.cpu()
    return model

def get_instruction(title, keywords):
    tokenizer = get_tokenier(special_tokens=SPECIAL_TOKENS)
    model = get_model(tokenizer, 
                    special_tokens=SPECIAL_TOKENS,
                    load_model_path='/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/src/model/instructions/pytorch_model.bin')

    kw = myDataset.join_keywords(keywords, randomize=False)

    prompt = SPECIAL_TOKENS['bos_token'] + title + \
            SPECIAL_TOKENS['sep_token'] + kw + SPECIAL_TOKENS['sep_token']
            
    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    device = torch.device('cpu')
    generated = generated.to(device)

    model.eval()

    # Beam-search text generation:
    sample_outputs = model.generate(generated, 
                                    do_sample=True, 
                                    # min_lenght= 50,  
                                    max_length=MAXLEN,
                                    # top_k=30,
                                    # top_p=0.7,
                                    # temperature=0.9,                                                      
                                    num_beams=5,
                                    repetition_penalty=5.0,
                                    early_stopping=True,      
                                    num_return_sequences=1
                                    )

    for i, sample_output in enumerate(sample_outputs):
        instruction = tokenizer.decode(sample_output, skip_special_tokens=True)
        a = len(title) + len(','.join(keywords))    
        # print("{}: {}\n\n".format(i+1,  instruction[a:]))
        # print("{}\n\n".format(instruction[a:]))
        return "{}\n\n".format(instruction[a:])

def get_ingredient(title, instruction):
    tokenizer = get_tokenier(special_tokens=SPECIAL_TOKENS)
    model = get_model(tokenizer, 
                    special_tokens=SPECIAL_TOKENS,
                    load_model_path='/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/src/model/ingredients/pytorch_model.bin')

    kw = myDataset.join_keywords(instruction, randomize=False)

    prompt = SPECIAL_TOKENS['bos_token'] + title + \
            SPECIAL_TOKENS['sep_token'] + kw + SPECIAL_TOKENS['sep_token']
            
    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    device = torch.device('cpu')
    generated = generated.to(device)

    model.eval()

    # Beam-search text generation:
    sample_outputs = model.generate(generated, 
                                    do_sample=True, 
                                    # min_lenght= 50,  
                                    max_length=MAXLEN,
                                    # top_k=30,
                                    # top_p=0.7,
                                    # temperature=0.9,                                                      
                                    num_beams=5,
                                    repetition_penalty=5.0,
                                    early_stopping=True,      
                                    num_return_sequences=1
                                    )

    for i, sample_output in enumerate(sample_outputs):
        ingredients = tokenizer.decode(sample_output, skip_special_tokens=True)
        a = len(title) + len(','.join(instruction))    
        # print("{}: {}\n\n".format(i+1,  ingredients[a:]))
        # print("{}\n\n".format(ingredients[a:]))
        return "{}\n\n".format(ingredients[a:])


title = "Tarte aux chocolats"
keywords = ['oeuf', 'farine', 'sucre', 'beurre', 'chocolat', 'noisette']

#test = get_instruction(title, keywords)
#print(test)
#print(type(test))

#test = get_instruction(title, keywords)
#print(test)
#print(type(test))
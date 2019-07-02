#importing libraries
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk import word_tokenize,pos_tag,sent_tokenize
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

helping_verbs=['am','is','are','was','were','being','been','be',
'have','has','had','do','does','did','will','would','shall','should','may','might','must','can','could']

main_verb_tags=['VBG','VB','VBD','VBZ','VBP']

nn_prp_tags=['NN','NNP','PRP',',','DT']

third_person_singular=['He','She','It']

wh_map={'PERSON':'Who','LOC':'Where','ORG':'Which','DATE':'When','TIME':'When','MONEY':'How much'}

entities=['PERSON','LOC','ORG','DATE','TIME','MONEY']

def reconstruct(list,tokens_tag):     #reconstructing list to sentence
   list[0]=list[0].title()
   if tokens_tag[-1][1]=='IN':
           del list[-1]

   list.append('?')        #adding question mark to the question 
   str1 = ' '.join(list)
   return str1

def yes_or_no_ques(text,tokens_tag):  #function for generating questions with boolean values as answers
   hv_flag=None
   new=[]
   if tokens_tag[0][1]=='PRP':
      text[0]=text[0].lower()    ## corrected only when pronoun is at the begining
   for i in range(0,len(tokens_tag)):    #loop for identifying helping verb
      if tokens_tag[i][0] in helping_verbs:
         hv_flag=i
         break
   if hv_flag!=None:    #framing question with a helping verb in sentence 
#      if text[hv_flag] in helping_verbs[14:]:
#         text[hv_flag]=text[hv_flag]+"n't"
      new.append(text[hv_flag])
      del text[hv_flag]
      for i in range(0,len(text)):
         new.append(text[i])
      return reconstruct(new,tokens_tag)
   else:           #framing question with out helping verb
      do_form=None
      main_verb=None
      subject=text[0]
      for i in range(0,len(tokens_tag)):  #loop for finding main verb
         if tokens_tag[i][1] in main_verb_tags:
            do_form=tokens_tag[i][1]  #identifying the tense of main verb
            main_verb=i
            break
      if do_form=='VBD':    #identifying appropriate do-form of the verb
         do_form='Did'      #do-form for past tense
      elif do_form=='VB':
         if subject in third_person_singular:      #do form for plural present tense form of the verb

           do_form='Does'
      else:                 #do form for singular present tense of the verb
         do_form='Do'
      new.append(do_form)
      text[main_verb]=lemmatizer.lemmatize(text[main_verb], pos='v')#obtaining main form of the verb
      for i in range(0,len(text)):
         new.append(text[i])
      return reconstruct(new,tokens_tag)

def identify_subject(text,tokens_tag):   ##identifies the subject
   for i in range(0,len(tokens_tag)):
      if tokens_tag[i][1] in nn_prp_tags and tokens_tag[i+1][1] not in nn_prp_tags:   #subject can be noun or a pronoun
         sub = i
         break
   remain=yes_or_no_ques(text[i:],tokens_tag[i:])       #we will use the next part of sentence for generating question
   return remain


def decompose(text,tokens_tag,ent_type):   ##function identifies each entity with it's corresponding Question word.
   print(identify_subject(text,tokens_tag))   ##Genenrating yes_or_no questions.
   for i in range(0,len(ent_type)):           ##Loop for generating questions on all possible entity types.
      temp=text[:]
      if ent_type[i][1] not in entities:   ##if entity is not recognized as a known entity
          continue
      if i == 0 :
          temp[i] = wh_map[ent_type[i][1]]      ##If entity is present in the subject of a sentence.
          print(reconstruct(temp,tokens_tag))
      
      elif ent_type[i][1] == 'PERSON':         ##If entity is present in the object of a sentence.
          place = text.index(ent_type[i][1])
          del temp[place]
          str = identify_subject(temp,tokens_tag)
          str = 'Whom'+" "+str.lower()
          print(str)
      else:
          place=text.index(ent_type[i][0])
          del temp[place]
          del tokens_tag[place]
          str = identify_subject(temp,tokens_tag)
          str = wh_map[ent_type[i][1]]+" "+str.lower()
          print(str)

                 

def main():
     text = "John is a studious boy. John parents are Robert and Alisha. John was born on 26th july 1999 in London. John got 80 percent ofmarks in his graduation. John works for microsoft and being paid a salary of $2000 per month. John goes to office at 9.00 AM in the morning and returns at 6:00 PM in the evening."
     sent = sent_tokenize(text)
     for i in range(0,len(sent)):      ##Generating possible questions from each sentence in the comprehension
         text1 = sent[i]     
         text1 = word_tokenize(text1)   ##Tokenization using nltk.
         tokens_tag = pos_tag(text1)
         print(tokens_tag)
         doc = nlp(sent[i])
         ent_type = []
         print(ent_type)
         for X in doc.ents:
            ent_type.append((X.text, X.label_))
            print(ent_type)
         decompose(text1,tokens_tag,ent_type)
if __name__ == '__main__':
  main()

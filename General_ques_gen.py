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

wh_map={'PERSON':'Who','LOC':'Where','ORGANIZATION':'Which','DATE':'When','TIME':'When','MONEY':'How much','PERCENT':'How much'}

entities=['PERSON','LOC','ORGANIZATION','DATE','TIME','MONEY','PERCENT']


def reconstruct(list,tokens_tag):     #reconstructing list to sentence
   list[0]=list[0].title()
   if tokens_tag[-1][1]=='IN':
           del list[-1]
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

def entity_recognizer():                            ##This function recognizes various entitytypes by merging 2 stanford classifiers

   with open('stanford-ner/7class.txt', 'r') as file:    ##LOading the file with names and entity types of 7 classes
       data7 = file.read().replace('\n', '')
   with open('stanford-ner/4class.txt', 'r') as file:    ##LOading the file with names and entity types of 4 classes
       data4 = file.read().replace('\n', '')
   data4=data4.split()
   data7=data7.split()
   new_list=[]
   for i in range(0,len(data4)):                         ## Merging two classifiers
       ent_4class=data4[i][data4[i].find('/')+1:]
       ent_7class=data7[i][data7[i].find('/')+1:]
       if(ent_7class=='O' and ent_4class!='O'):
          ent_7class=ent_4class
       new_list.append((data7[i][:data7[i].find('/')],ent_7class))    ##  the entity and it's type based on two classifiers
   return new_list  


## preprocessing for grouping the consecutive answer words
 ## This function returns the index of final word up to which we consider as an answer phrase
def group_ind(text,ent_type,prev_type,place):           
   group_index=place
   for j in range(place,len(ent_type)):
       if ent_type[j][1]==prev_type or text[j]=='and' or text[j]==',':
           group_index+=1;
   return group_index

def decompose(text,tokens_tag,ent_type):           ##function identifies each entity with it's corresponding Question word.
   print(identify_subject(text,tokens_tag))        ##Genenrating yes_or_no questions.
   prev=None
   for i in range(len(ent_type)):                 ##Loop for generating questions on all possible entity types.
      try: 
        place = text.index(ent_type[i][0])
      except:
        continue
      group_index=group_ind(text,ent_type,ent_type[i][1],place)
      temp=text[:]
      if ent_type[i][1] not in entities :          ##if entity is not recognized as a known entity
           
          continue
      prev=ent_type[i][1]
      if i == 0 :
          temp[i] = wh_map[ent_type[i][1]]      ##If entity is present in the subject of a sentence.
          print(reconstruct(temp,tokens_tag))

      elif ent_type[i][1] == 'PERSON' and i>0 :         ##If entity is present in the object of a sentence.
          
     #    place = text.index(ent_type[i][0])
     #     group_index=group_ind(text,ent_type,ent_type[i][1],place)
          del temp[place:group_index]
          str = identify_subject(temp,tokens_tag)
          str = 'Whom'+" "+str.lower()
          print(str)
      else:
          
          del temp[place:group_index]
          str = identify_subject(temp,tokens_tag)
          str = wh_map[ent_type[i][1]]+" "+str.lower()
          print(str)
      if place==group_index:
         i=i+1
      else:
         i=group_index     

def preprocess(text1):
     new_text=[]
     for i in range(len(text1)):
       str=text1[i]
       prev=0
       for j in range(len(str)):
          if str[j]==',' and j<len(str):
            new_text.append(str[prev:j])
            prev=j+1
          elif j==len(str):
            new_text.append(str)
     print(text1)
     print(new_text)
     return new_text


def main():
     with open('stanford-ner/sample.txt', 'r') as file:
       text = file.read().replace('\n', '')
     length=0
     sent = sent_tokenize(text)
     for i in range(0,len(sent)):      ##Generating possible questions from each sentence in the comprehension
         text1 = sent[i] 
         text1 = word_tokenize(text1)
         tokens_tag = pos_tag(text1)
         ent_type = []
         ent_type=entity_recognizer()
  #       answer_identifier(text1,ent_type[length:length+len(text1)])
         decompose(text1,tokens_tag,ent_type[length:length+len(text1)])
         length+=len(text1)
if __name__ == '__main__':
   main()

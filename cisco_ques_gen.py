#importing libraries
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk import word_tokenize,pos_tag,sent_tokenize


helping_verbs=['am','is','are','was','were','being','been','be',
'have','has','had','do','does','did','will','would','shall','should','may','might','must','can','could']

main_verb_tags=['VBG','VB','VBD','VBZ','VBP']

nn_prp_tags=['NN','NNP','PRP',',','DT']

third_person_singular=['He','She','It']

wh_map={'SWITCH':'Which switches','PMA':'Which','NET_TYPE':'Which','PRODUCT':'Which product','HW_FEATURE':'Which feature','SW_FEATURE':'Which feature','MODULE':'What','VERSION':'Which version','CONFIG':'What configuration','DLRIL':'Which','SOFTWARE':'What','COMMAND':'Which','LICENCE':'What','CAPABILITIES':'What','LAYERS':'Which layers','ARCHITECTURE':'What architecture','POWER_MODE':'What'}

entities=['SWITCH','PMA','NET_TYPE','PRODUCT','HW_FEATURE','SW_FEATURE','MODULE','VERSION','CONFIG','DLRIL','SOFTWARE','COMMAND','LICENCE','CAPABILITIES','LAYERS','ARCHITECTURE','POWER_MODE']


def reconstruct(list,tokens_tag):     #reconstructing list to sentence
   list[0]=list[0].title()
   if tokens_tag[-1][1]=='IN':
           del list[-1]
   del list[-1]
   list.append('?')         #adding question mark to the question 
   str1 = ' '.join(list)
   return str1

def yes_or_no_ques(text,tokens_tag):  #function for generating questions with boolean values as answers
   hv_flag=None
   new=[]
   if tokens_tag[0][1]=='PRP':
      text[0]=text[0].lower()                   ## corrected only when pronoun is at the begining
   for i in range(0,len(tokens_tag)):           ##loop for identifying helping verb
      if tokens_tag[i][0] in helping_verbs:
         hv_flag=i
         break
   if hv_flag!=None:                           #framing question with a helping verb in sentence 
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
      for i in range(0,len(tokens_tag)):        #loop for finding main verb
         if tokens_tag[i][1] in main_verb_tags:
            do_form=tokens_tag[i][1]               #identifying the tense of main verb
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

def identify_subject(text,tokens_tag):       ##identifies the subject
   for i in range(0,len(tokens_tag)):
      if tokens_tag[i][1] in nn_prp_tags and tokens_tag[i+1][1] not in nn_prp_tags:   #subject can be noun or a pronoun
         sub = i
         break
   remain=yes_or_no_ques(text[i:],tokens_tag[i:])       #we will use the next part of sentence for generating question
   return remain

def entity_recognizer():                            ##This function recognizes various entitytypes by merging 2 stanford classifiers

   with open('stanford-ner/cisco_ent.txt', 'r') as file:    ##LOading the file with names and entity types of 7 classes
       data = file.read().replace('\n', '')
   data=data.split()
   new_list=[]
   for i in range(0,len(data)):                         ## Merging two classifiers
       ent_class=data[i][data[i].find('/')+1:]
       new_list.append((data[i][:data[i].find('/')],ent_class))    ##  the entity and it's type based on two classifiers
   return new_list  


## preprocessing for grouping the consecutive answer words

def group_ind(text,ent_type,prev_type,place):            ## This function returns the index of 
   group_index=place
   for j in range(place,len(ent_type)):
       if ent_type[j][1]==prev_type or text[j]=='and' or text[j]==',':
           group_index+=1;
   return group_index

def decompose(text,tokens_tag,ent_type):           ##function identifies each entity with it's corresponding Question word.
                                              
   prev=None
   i=0
   for i in range(len(ent_type)):                ##Loop for generating questions on all possible entity types.
      try: 
        place = text.index(ent_type[i][0])
      except:
        continue
      group_index=group_ind(text,ent_type,ent_type[i][1],place)  ##identyfing entities of same type as a group 
      temp=text[:]
      if ent_type[i][1] not in entities :          ##if entity is not recognized as a known entity
          continue
      else :
         yes_no=identify_subject(text,tokens_tag)                     ##Generating wh_questions  
         print(yes_no)        
         sub= temp[place:group_index]        
         yes_no=word_tokenize(yes_no)
         del yes_no[(1+place):group_index]                          ##removing answer phrases
         try:
           if yes_no[place+1].lower()==wh_map[ent_type[i][1]].split(' ')[1]:         #preprocessing
              del yes_no[place+1]
         except:
           delete=None
         yes_no = ' '.join(yes_no)
         str = wh_map[ent_type[i][1]]+" "+yes_no.lower()
         print(str)    
      i=group_index+1
      
         

def main():
     with open('stanford-ner/cisco.txt', 'r') as file:
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

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

def reconstruct(list):     #reconstructing list to sentence
   list[0]=list[0].title()
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
      return reconstruct(new)
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
      return reconstruct(new)

def identify_subject(text,tokens_tag):   ##identifies the subject
   for i in range(0,len(tokens_tag)):
      if tokens_tag[i][1] in nn_prp_tags and tokens_tag[i+1][1] not in nn_prp_tags:   #subject can be noun or a pronoun
         sub=i
         break
   remain=yes_or_no_ques(text[i:],tokens_tag[i:])       #we will use the next part of sentence for generating question
   return remain

def main():
   text=input("Enter sentence : ")
   text=sent_tokenize(text)

   for i in range(0,len(text)):
     print(text[i])
     text1=word_tokenize(text[i])     #word-tokenzing
     tokens_tag=pos_tag(text1)     #pos-tagging
     str=identify_subject(text1,tokens_tag)
     print(str)
if __name__ == '__main__':
  main()

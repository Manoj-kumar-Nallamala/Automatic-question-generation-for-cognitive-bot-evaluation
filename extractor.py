import nltk
from nltk import word_tokenize,pos_tag,sent_tokenize


def remove_appos(tokens_tag,text):#function to remove appositive(',') and elminating the relative pronouns
  index_of_appos=None
  for i in range(0,len(tokens_tag)-1):
      if tokens_tag[i][1]=='NNP' and tokens_tag[i+1][0]==',':#finding if appositive (',')present after noun phrase
        index_of_appos=i+1
        break
  if index_of_appos!=None:
     text[index_of_appos]='is'#eliminating appositive(',')
     wrb_flag=0#presence of relative adverb
     if tokens_tag[index_of_appos+1][1]=='WP' or tokens_tag[index_of_appos+1][1]=='WRB':
        if tokens_tag[index_of_appos+1][1]=='WRB':
            wrb_flag=1
        del text[index_of_appos+1]#removing relative pronoun for nouns('who')
        del text[index_of_appos]
        if wrb_flag==1:#removing relative pronoun for nouns('where')
          new=text[:]
          new=new[index_of_appos:]
          new.append('in')
          new.append(text[0])
          text=new[:]
  return text

  
  
def remove_modifiers(text):
  #removing non restrictive appositive (,) after the subject
  text=word_tokenize(text)
  tokens_tag = pos_tag(text)
  print(tokens_tag)
  text=remove_appos(tokens_tag,text)
  print(text)


def main():
   str0="Hyderabad,where the charminar is located"
   str1="Jeff,the president of USA"
   str2="Jeff,who was the president of USA"
   modified_sentence=remove_modifiers(str0)
   modified_sentence=remove_modifiers(str1)
   modified_sentence=remove_modifiers(str2)
   print(modified_sentence)

if __name__ == '__main__':
    main()

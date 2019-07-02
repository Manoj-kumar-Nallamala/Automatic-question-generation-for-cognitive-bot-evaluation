def answer_identifier(text,ent_type):                  #This function identifies the answers on which question phrases can be mapped.
    answers=[]
    print(text)
    print(ent_type)
    str=None
    prev_type=None
    for i in range(0,len(text)):
       if prev_type!=None:
         if text[i] =='and' or text[i]==',':
             str+=text[i]
             print(prev_type)
             print('and')
             print(str)

       if ent_type[i][1]!='O':
         if ent_type[i][1] in entities and prev_type!=ent_type[i][1]:
            str=text[i]
            print(str)
            prev_type=ent_type[i][1]
         elif ent_type[i][1] in entities and prev_type==ent_type[i][1]:
            str+=text[i]
            print(str)
       else:
          if str!='':
            answers.append(str)
            str=''
            prev_type=None

    print(answers)


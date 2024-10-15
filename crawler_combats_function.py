from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
from functools import reduce
from time import sleep



def find_script(tag):
    if re.fullmatch(r'adh\(\d+\,\d+\,\"[0-9][0-9]:[0-9][0-9]\"\,\d+\)',tag.get_text()):
        return tag
    else:
        None
def find_b(tag):
    if 'class' in tag.attrs and tag['class']!=[]:
        if re.fullmatch(r'b\d+',*tag['class']):
            return tag
        else:
            return None
    return None
def getLinks(articleUrl):
    global pages
    team={}

    result={}
    
    priem=['Кристаллизации','Колотых ран','Магической раны','Двойной бросок','Живой Искры','Мясорубка','Глубоких порезов','Броском топора','Оледенения','Отравления','Ядовитого Пузыря','Метеорита','Огненному Щиту','Астральный удар','Пожирающего Пламени']#,'Сгусток чудовищной энергии']
    #priem=['Свиток продвинутого лечения', 'Ставка на опережение', 'Зоркий глаз x 3', 'Каменный Цветок', 'Раскрыть намерения', 'Резерв сил', 'Глубоких порезов', 'Ярость x 2', 'Призрачная защита', 'Ускоренные рефлексы', 'Дикая удача', 'Шокирующий удар', 'Божественный щит', 'Восстановление энергии 750HP', 'Отражение Ненависти', 'Пожирающего Пламени', 'Булыжник', 'Точные стрелы в действии x 3', 'Тяжелый таран', 'Курс превентивной защиты.', 'Тяжелый таран x 2', 'Натиск', 'Агрессивная защита', 'Каменный Удар', 'Курс точных стрел.', 'Тактика Парирования', 'Пылающий Ужас', 'Сотрясение мозга', 'Точный удар', 'Оглушающий выстрел', 'Песчаный Щит', 'Стойкость x 2', 'Кристаллизация Гиганта', 'Магический Барьер', 'Стойкость', 'Жажда Крови x 2', 'Проникающие удары', 'Уплотнение покрова', 'Выбор противника', 'Скрытое Пламя', 'Двойной бросок', 'Восстановление энергии 600HP', 'Превосходство', 'Жажда Крови', 'Отравления', 'Привентивная защита в действии x 2', 'Пожирающее Пламя', 'Светлое Очищение', 'Огненный Щит', 'Озарение', 'Толстая шкура', 'Кинетический Барьер', 'Огненное Покровительство', 'Точные стрелы в действии', 'Огненному Щиту', 'Тактическое мышление', 'Глубокие порезы', 'Привентивная защита в действии x 3', 'Стойкость x 3', 'Точные стрелы в действии x 2', 'Полная защита', 'Тлеющий пепел', 'Обреченность', 'Тактика Атаки', 'Испепеление', 'Тактика Крита', 'Метеорита', 'Магическое озарение', 'Разгадать тактику', 'Жажда Крови x 3', 'Зоркий глаз x 2', 'Скрытая ловкость', 'Язык Пламени', 'Аура Царя Цветов', 'Оледенения', 'Исцеление 25%', 'Свиток тяжелого тарана', 'Ярость x 3', 'Слепая удача', 'Свиток толстой шкуры', 'Мясорубка', 'Разогрев', 'Стремительные стрелы', 'Привентивная защита в действии', 'Ядовитого Пузыря', 'Броском топора', 'Усиленные удары', 'Вспышка', 'Тактический просчет', 'Зоркий глаз', 'Медитация', 'Живой Искры', 'Метеорит', 'Глоток магии', 'Астральный удар', 'Восстановление энергии 450HP', 'Тактика Защиты', 'Ярость']
    health=['Исцеление','Кровавый Поток','Собрать Зубы','Восстановление энергии ','Выжить','Отменить', 'Утереть Пот']
    html =urlopen('https://capitalcity.combats.com/logs.pl?log={}'.format(articleUrl))
    bs = BeautifulSoup(html, 'html.parser')
    
    rr=bs.find_all('h3')[0].find_all('a')

    rr=[r for r in rr if 'href' in r.attrs and r['href'].startswith('log')]
    
    for page in range(1,int(rr[-2].get_text())+2):

        ldict={}
        ldict_v2={}
   
        bs=BeautifulSoup(urlopen('https://capitalcity.combats.com/logs.pl?log={}&p={}'.format(articleUrl,page)))
        bs_script=bs.find_all(find_script)
        bs_time=bs.find_all('font',{'class':['date','sysdate']})     
        #print('SCRIPT',bs_script)
        bs_b=bs.find_all(find_b)
        for i in range(len(bs_b)):
            key,value=bs_b[i]['class'][0],bs_b[i].get_text()
            l=team.get(key,[])
            if value not in l:
                l.append(value)
            team[key]=l
        
        #print('STRONG',bs.find_all('strong'))
        priem.extend([re.sub(r'\s\[\d+\]','',b.get_text())  for b in bs.find_all('strong')])
        priem=list(set(priem))
        print(priem)
        for t in list(reduce(lambda x,y:x+y,[v for v in team.values()])):
            if t not in result.keys():
                 result[t]=dict(zip(list(reduce(lambda x,y:x+y,[v for v in team.values()])),[0 for r in range(len(list(reduce(lambda x,y:x+y,[v for v in team.values()]))))]))
                 for k in result.keys():
                     result[k][t]=0
        temp_string=' '.join([b.strip('\n\xa0') for b in bs.form.find_all(string=True) if b!='\n'])[:' '.join([b.strip('\n\xa0') for b in bs.form.find_all(string=True) if b!='\n']).find('Страницы')]
        #temp_string_v2=re.sub(r'adh\(\d+\,\d+\,\"[0-9][0-9]:[0-9][0-9]\"\,\d+\)',r'',' '.join([b.strip('\n\xa0') for b in bs.form.find_all(string=True) if b!='\n'])[:' '.join([b.strip('\n\xa0') for b in bs.form.find_all(string=True) if b!='\n']).find('Страницы')])      
        if bs_script:
            last_key=bs_script[-1]
            ldict_values=[re.split('[0-9][0-9]:[0-9][0-9]',bb) for bb in re.split('adh\(\d+\,\d+\,\"[0-9][0-9]:[0-9][0-9]\"\,\d+\)',temp_string)]
            for i in range(len(ldict_values[1:])):
                    key,value=bs_script[i],ldict_values[1:][i]
                    l=ldict.get(key,[])
                    l.extend(value)
                    ldict[key]=l
            ldict[last_key].extend(ldict_values[0])
            
        else:
            print('ELSE')
            ldict_keys=[last_key]
            
            ldict_values=re.split('[0-9][0-9]:[0-9][0-9]',temp_string)#' '.join([b.strip('\n') for b in bs.form.find_all(string=True) if b!='\n']))
            ldict[last_key]=ldict_values   
        regex=('|').join(list(reduce(lambda x,y:x+y,[v for v in team.values()])))+'|'+r'\.\s+.\d+'
        
        print('TEGEXDD',regex)
        for key, value in ldict.items():
            for v in value:   
                if re.findall(r'\d+\/\d+',v) and v.find('Мана')==-1 and v.find('Исцеление')==-1 and v.find('регенерирует здоровье')==-1 and not re.findall(r'\s+--',v) and not re.findall(r'\.\s+--',v) and not re.findall('|'.join(health),v):
                    print(key.get_text(),':',v,'\n')
                    print([m[0] for m in re.finditer(regex,v)])
                    string_list=[m[0] for m in list(re.finditer(regex,v))]
                    #print(string_list)
                    if re.findall('зверь',v):
                        for i in range(len(string_list)):
                            tstr='(зверь '+string_list[i]+')'
                            name=r'[А-Яа-яa-zA-z]+ \(зверь '
##                            print(tstr)
##                            print('fbr',re.findall(name,v)[0][:-7])
                            if re.findall(tstr,v):
                                string_list[i]=re.findall(name,v)[0][:-6] +'зверь '+string_list[i]+')'
##                                print('m',string_list[i])
##                        print(string_list)        
##                        input()
                    #string_list=list(re.finditer(regex,v))
                    # 
                    if len(string_list)==3:
                        print('3')
##                        
                        if re.findall('|'.join(priem),v):
                          
                            if string_list[2][1:].strip()[0]=='-':                                
                                result[string_list[0]][string_list[1]]+=int(string_list[2][1:].strip()[1:])                                 
                            else:
                                result[string_list[1]][string_list[0]]+=int(string_list[2][1:].strip()[1:])

                        else:    
                            if string_list[2][1:].strip()[0]=='-':
                                if not re.findall(r'травм|поврежден',v):
                                    result[string_list[1]][string_list[0]]+=int(string_list[2][1:].strip()[1:])
                                else:
                                    result[string_list[0]][string_list[1]]+=int(string_list[2][1:].strip()[1:]) 
                            else:
                                result[string_list[0]][string_list[1]]+=int(string_list[2][1:].strip()[1:])
                        print('temp',result)
                    elif len(string_list)==2:
                        if (string_list[0] not in (list(reduce(lambda x,y:x+y,[v for v in team.values()])))) or (string_list[1] not in (list(reduce(lambda x,y:x+y,[v for v in team.values()])))):
                            print('2')
                            
                            if len([p for p in priem if v.find(p)!=-1])>0:
                                print('PR')
                                sleep(3)
                                for bs_t in bs_time:
                                    a=bs_t.next_sibling.next_sibling.next_sibling.next_sibling
                                    b=bs_t.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
                                    if a.name=='b' and a.get_text()==[p for p in priem if v.find(p)!=-1][0]:
                                        print(a)
                                        if b.name=='font' and 'title' in b.attrs and b.b.get_text()==string_list[1][1:].strip():
                                            bs_font=b
                                            print('bs',bs_font)
                                            break                 
                            else:
                                bs_font=''
                                for bs_t in bs_time:
                                    a=bs_t.next_sibling.next_sibling.next_sibling.next_sibling
                                    if a.name=='font' and 'title' in a.attrs and a.b.get_text()==string_list[1][1:].strip():
                                        bs_font=a
                                        print('bs',bs_font)
                                        break


                            if string_list[1][1:].strip()[0]=='-':
                                
                                result[bs_font['title'][bs_font['title'].find('b')+2:bs_font['title'].find('/b')-1]][string_list[0]]+=int(string_list[1][1:].strip()[1:])
                            else:
                                result[string_list[0]][bs_font['title'][bs_font['title'].find('b')+2:bs_font['title'].find('/b')-1]]+=int(string_list[1][1:].strip()[1:])
                       
                            print('temp',result)
                            
                        else:
                            if v.find('казнил')!=-1:
                                result[string_list[0]][string_list[1]]+=int(list(re.finditer(r'\s+.\d+',v))[0][0][1:].strip()[1:])
                                print('2-res',result)
                                
                    elif len(string_list)==1:
                        print('1')
                        for bs_t in bs_time:
                            a=bs_t.next_sibling.next_sibling.next_sibling.next_sibling
                            b=bs_t.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
                            if a.name=='b' and a.get_text()==[p for p in priem if v.find(p)!=-1][0]:
                                if b.name=='font' and 'title' in b.attrs and b.b.get_text()==re.findall(r'\s+.\d+',v)[0].strip():
                                    bs_font=b
                                    print('bs',bs_font)

                        if list(re.findall(r'\s+.\d+',v))[0].strip()[0]=='-':
                            result[bs_font['title'][bs_font['title'].find('b')+2:bs_font['title'].find('/b')-1]][string_list[0]]+=int(list(re.findall(r'\s+.\d+',v))[0].strip()[1:])
                        else:
                            result[string_list[0]][bs_font['title'][bs_font['title'].find('b')+2:bs_font['title'].find('/b')-1]]+=int(list(re.findall(r'\s+.\d+',v))[0].strip()[1:])
                        print('2-res',result)
                

        print('--------------------------------------------------------------------------------', page)
        #input()
    return result
            
#1695231693.2218
for key, value in getLinks('1722534791.95469').items():
    print ('Персонаж ',key,':',sum(value.values()))
    for k,v in value.items():
        print ( k,':',v,'\n')

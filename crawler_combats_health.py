from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
from functools import reduce
from time import sleep
import requests



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
    team = {}

    result = {}
    result_hill = {}
    
    priem=['Кристаллизации','Колотых ран','Магической раны','Двойной бросок','Живой Искры','Мясорубка','Глубоких порезов',
           'Броском топора','Оледенения','Отравления','Ядовитого Пузыря','Метеорита','Огненному Щиту','Астральный удар',
           'Ядовитого Взрыва' ,'Пожирающего Пламени']#,'Сгусток чудовищной энергии']
    #priem=['Свиток продвинутого лечения', 'Ставка на опережение', 'Зоркий глаз x 3', 'Каменный Цветок', 'Раскрыть намерения', 'Резерв сил', 'Глубоких порезов', 'Ярость x 2', 'Призрачная защита', 'Ускоренные рефлексы', 'Дикая удача', 'Шокирующий удар', 'Божественный щит', 'Восстановление энергии 750HP', 'Отражение Ненависти', 'Пожирающего Пламени', 'Булыжник', 'Точные стрелы в действии x 3', 'Тяжелый таран', 'Курс превентивной защиты.', 'Тяжелый таран x 2', 'Натиск', 'Агрессивная защита', 'Каменный Удар', 'Курс точных стрел.', 'Тактика Парирования', 'Пылающий Ужас', 'Сотрясение мозга', 'Точный удар', 'Оглушающий выстрел', 'Песчаный Щит', 'Стойкость x 2', 'Кристаллизация Гиганта', 'Магический Барьер', 'Стойкость', 'Жажда Крови x 2', 'Проникающие удары', 'Уплотнение покрова', 'Выбор противника', 'Скрытое Пламя', 'Двойной бросок', 'Восстановление энергии 600HP', 'Превосходство', 'Жажда Крови', 'Отравления', 'Привентивная защита в действии x 2', 'Пожирающее Пламя', 'Светлое Очищение', 'Огненный Щит', 'Озарение', 'Толстая шкура', 'Кинетический Барьер', 'Огненное Покровительство', 'Точные стрелы в действии', 'Огненному Щиту', 'Тактическое мышление', 'Глубокие порезы', 'Привентивная защита в действии x 3', 'Стойкость x 3', 'Точные стрелы в действии x 2', 'Полная защита', 'Тлеющий пепел', 'Обреченность', 'Тактика Атаки', 'Испепеление', 'Тактика Крита', 'Метеорита', 'Магическое озарение', 'Разгадать тактику', 'Жажда Крови x 3', 'Зоркий глаз x 2', 'Скрытая ловкость', 'Язык Пламени', 'Аура Царя Цветов', 'Оледенения', 'Исцеление 25%', 'Свиток тяжелого тарана', 'Ярость x 3', 'Слепая удача', 'Свиток толстой шкуры', 'Мясорубка', 'Разогрев', 'Стремительные стрелы', 'Привентивная защита в действии', 'Ядовитого Пузыря', 'Броском топора', 'Усиленные удары', 'Вспышка', 'Тактический просчет', 'Зоркий глаз', 'Медитация', 'Живой Искры', 'Метеорит', 'Глоток магии', 'Астральный удар', 'Восстановление энергии 450HP', 'Тактика Защиты', 'Ярость']
    health=['Исцеление','Кровавый Поток','Собрать Зубы','Восстановление энергии ','Выжить','Отменить', 'Утереть Пот']
    html =urlopen('https://capitalcity.combats.com/logs.pl?log={}'.format(articleUrl))
    bs = BeautifulSoup(html, 'html.parser')
    
    rr = bs.find_all('h3')[0].find_all('a')

    rr = [r for r in rr if 'href' in r.attrs and r['href'].startswith('log')]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
    for page in range(1, int(rr[-2].get_text())+2):
        ldict = {}
        ldict_v2 = {}
        #sleep(5)
        rs = requests.get('https://capitalcity.combats.com/logs.pl?log={}&p={}'.format(articleUrl, page), headers=headers)
        #bs = BeautifulSoup(urlopen('https://capitalcity.combats.com/logs.pl?log={}&p={}'.format(articleUrl, page)))
        bs = BeautifulSoup(rs.text, 'html.parser')
        bs_script = bs.find_all(find_script)
        bs_time = bs.find_all('font',{'class':['date','sysdate']})
        #print('SCRIPT',bs_script)
        bs_b = bs.find_all(find_b)
        for i in range(len(bs_b)):
            key, value = bs_b[i]['class'][0], bs_b[i].get_text()
            l = team.get(key, [])
            if value not in l:
                l.append(value)
            team[key] = l
        
        #print('STRONG',bs.find_all('strong'))
        priem.extend([re.sub(r'\s\[\d+\]','', b.get_text()) for b in bs.find_all('strong')])
        priem = list(set(priem))
        #print(priem)
        for t in list(reduce(lambda x, y: x + y, [v for v in team.values()])):
            if t not in result.keys():
                 result[t] = dict(zip(list(reduce(lambda x, y: x + y, [v for v in team.values()])), [0 for r in range(len(list(reduce(lambda x,y:x+y,[v for v in team.values()]))))]))
                 for k in result.keys():
                     result[k][t]=0
        ids1 = ''.join([b.strip('\n\xa0') for b in bs.find_all(string=True) if b != '\n']).find('Страницы')+len('Страницы')
        temp_ids1 = ''.join([b.strip('\n\xa0') for b in bs.find_all(string=True) if b != '\n'])[ids1:]
        temp_string = temp_ids1[:temp_ids1.find('Страницы')]
        health_list = ['Восстановление энергии', 'Исцеление 25%', 'Исцеление 10%', 'Исцеление 50%', 'Исцеление 100%']
        #print(temp_string)
        if bs_script:
            last_key = bs_script[-1]
            ldict[last_key] = []
            ldict_values = [re.split('[0-9][0-9]:[0-9][0-9]', bb) for bb in re.split('adh\(\d+\,\d+\,\"[0-9][0-9]:[0-9][0-9]\"\,\d+\)', temp_string)]
            #ldict_values = [[lvl for lvl in lval if lvl.find('Восстановление энергии')!=-1] for lval in ldict_values]
            ldict_values = [[lvl for lvl in lval if re.findall('|'.join(health_list), lvl)] for lval in ldict_values]
            print(ldict_values)
            input()
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
       
        print('TEGEXDD', regex)
        for key, value in ldict.items():
            for v in value:
                print('VVVV', v)
                
                if re.findall(r'\d+\/\d+',v) and not re.findall(r'\s+--',v) and not re.findall(r'\.\s+--',v):# and re.findall('|'.join(health),v):
                    # and v.find('Мана')==-1 and v.find('Исцеление')==-1 and v.find('регенерирует здоровье')==-1
                    print('KGETTEXT',key.get_text(),':',v,'\n')
                    
                    print('FUNDITER', [m[0] for m in re.finditer(regex,v)])
                    string_list=[m[0] for m in list(re.finditer(regex,v))]
                    type_hill = [vv for vv in v.split('"') if vv.find('Восстановление')!=-1][0].split()[-1]
                    print('TYPE_HILL',type_hill)
                    #print(string_list)
                    if len(string_list)==2:
                        hill = int(string_list[1].strip('.'))
                        if not result_hill.get(string_list[0]):
                            result_hill[string_list[0]] = {}
                        if result_hill[string_list[0]].get(type_hill):
                            result_hill[string_list[0]][type_hill]['count'] +=1
                            result_hill[string_list[0]][type_hill]['summ'] += hill
                        else:
                            result_hill[string_list[0]][type_hill]={'count': 0, 'summ': 0}
                            result_hill[string_list[0]][type_hill]['count'] += 1
                            result_hill[string_list[0]][type_hill]['summ'] += hill

                       
        print('--------------------------------------------------------------------------------', page)
        #input()
    return result_hill
            
#1695231693.2218
for key, value in getLinks('1722533412.518').items():
##    print(value.values())
##    print([val['summ'] for val in value.values()])
    print ('Персонаж ',key,':', sum([val['summ'] for val in value.values()]))
    for k,v in value.items():
        print ( k,':', v['summ'] ,'\n')

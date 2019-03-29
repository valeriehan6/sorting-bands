#!/usr/bin/env python3
import random
import csv
import itertools
import numpy
from itertools import cycle
import copy
#from more_itertools import sort_together

genre_array=['Hip-Hop/R&B', 'Rock', 'Jazz', 'Singer/Songwriter', 'Electronic']
skills_array=['Producer/beatmaker', 'Acoustic Guitar', 'Bass Guitar', 'Electric Guitar', 'Piano', 'Singer', 'Rapper', 'Drumset/percussion', 'Saxophone', 'Upright Bass', 'Trumpet', 'Trombone', 'Other']

class musician:
    def __init__(self, name,prim_genres, skills, proficiencies, sec_genres=None):
        self.name=name
        self.genre=prim_genres
        self.secondary=sec_genres
        self.skills=skills
        self.level=proficiencies
        self.assigned=False
        if type(self.skills)==list:
            ordered_skills = [x for _,x in sorted(zip(self.level,self.skills), reverse=True)]
            order=[sorted(self.level, reverse=True)]
            self.level=order
            self.skills=ordered_skills
        
    def __str__(self):
        return repr(self)
        
    def __repr__(self):
        to_string='Name: ' + self.name
        to_string+=' |Primary Genre: '+self.genre
        if type(self.skills)==list:
            to_string+=' |Skills: ' + ', '.join(self.skills)
            to_string+=' |Proficiencies: ' + ', '.join([str(x) for x in self.level])
        else:
            to_string+=' |Skills: ' + self.skills
            to_string+=' |Profficiences: ' + str(self.level)
        if self.secondary != None:
            if type(self.secondary)==list:
                to_string+=' |Secondary Genres: ' + ', '.join(self.secondary)
            else:
                to_string+=' |Seondary Genres: ' + self.secondary
        return to_string
            
class group:
    def __init__(self, genre, musicians, skills):
        
        self.genre=genre
        self.iscomplete=False
        self.skills=skills
        self.musician_array=musicians
        self.checkComplete()
        #self.musician_array.append(musicians)
    
    def add_musician(self, musician, skill):
        self.musician_array.append(musician)
        self.skills.append(skill)
        musician.assigned=True
    def remove_musician(self, musician):
        loc=self.musician_array.index(musician)
        self.musician_array.remove(musician)
        self.skills.pop(loc)
        #self.checkComplete()
        
    def __repr__(self):
        to_string='Group Type: ' + self.genre + '\n'
        to_string+='\n'.join([repr(x) for x in self.musician_array])
        return to_string
    def get_avgprofs(self):
        profs=[]
        for i in range(len(self.musician_array)):
            m=self.musician_array[i]
            s=self.skills[i]
            
            loc=m.skills.index(s)
            
            #profs.append((m.transform_prof()[loc]))
        return(numpy.mean(profs))
            
    def checkComplete(self):
        
        self.iscomplete=False
        num_prod=len([x for x in self.musician_array if 'Producer/beatmaker' in x.skills])
        num_perc=len([x for x in self.musician_array if 'Drumset/percussion' in x.skills])
        num_singers=len([x for x in self.musician_array if 'Singer' in x.skills])
        num_guitars=len([x for x in self.musician_array if 'Acoustic Guitar' in x.skills]) + len([x for x in self.musician_array if 'Electric Guitar' in x.skills])
        num_bassG=len([x for x in self.musician_array if 'Bass guitar' in x.skills])
        
        
        #self.iscomplete=False
        
        if (self.genre=='Hip-Hop/R&B'):
            if (num_prod>=1 and num_rappers >=1):
                self.iscomplete=True  
        
        elif (self.genre=='Rock'):######################
            #print(num_perc)
            #print(num_singers)
            #print(num_guitars)
            if ((num_perc>=1) and num_singers>=1 and num_guitars>=1):
                self.iscomplete=True
        
        elif (self.genre=='Jazz'):##########################
            num_horn=len([x for x in self.musician_array if 'Saxophone' in x.skills]) + len([x for x in self.musician_array if 'Trumpet' in x.skills]) + len([x for x in self.musician_array if 'Trombone' in x.skills])
            num_dBass=len([x for x in self.musician_array if 'Upright Bass' in x.skills])
            num_piano=len([x for x in self.musician_array if 'Piano' in x.skills])

            if (num_perc>=1 and num_horn>=1 and (num_dBass>=1 or num_bassG>=1 or num_piano>=1)):
                self.iscomplete=True

        elif (self.genre=='Singer/Songwriter'):########################
            if(num_singers>=1 and len(self.musician_array)>=2):
                self.iscomplete=True

        elif(self.genre=='Electronic'):
            if(num_prod>=1 and len(self.musician_array)>=2):
                self.iscomplete=True
        
        return self.iscomplete
          
def gen_rand_musician(name):
    num_sec_genres=random.randint(0,3)
    rand_genre=random.sample(genre_array, 1)[0]
    if(num_sec_genres!=0):
        rand_genre=random.sample(genre_array, 1)[0]
        rand_sec_genres=random.sample(genre_array, num_sec_genres)   

        while(rand_genre in rand_sec_genres):
            rand_sec_genres.remove(rand_genre)
    else:
        rand_sec_genres=None
       
    num_skills=random.randint(1,3)
    rand_skills=random.sample(skills_array, num_skills)
    rand_proficiencies=random.sample(proficiency_array, num_skills)
    
    return musician(name,rand_genre, rand_skills, rand_proficiencies, rand_sec_genres)

def gen_musician_array(num_musicians):
    musician_array=[]
    for i in range(num_musicians):
        musician_array.append(gen_rand_musician(str(i)))
    return musician_array
    
def write_musicians(filename, musicians):
    with open(filename, 'wt') as f:
        csvwriter=csv.writer(f, delimiter='\n')
        csvwriter.writerow(musicians)

def write_groups(filename, groups):
    with open(filename, 'wt') as f:
        csvwriter=csv.writer(f, delimiter='\n')
        csvwriter.writerow(groups)

def read(file_name):
    m_array=[]
    
    with open(file_name, encoding='cp1252') as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',')
        rownum=0
        for row in csvReader:
            if rownum!=0:
                skills=[]
                levels=[]
                if row[12]!='':
                    t=[x.strip() for x in row[12].split(';')]
                    skills=skills+t
                    #print(len(t))
                    for val in t:
                        levels.append(15)
                if row[11]!='':
                    t=[x.strip() for x in row[11].split(';')]
                    skills=skills+t
                    #print(len(t))
                    for val in t:
                        levels.append(13)
                if row[10]!='':
                    #print(len(t))
                    t=[x.strip() for x in row[10].split(';')]
                    skills=skills+t
                    for val in t:
                        levels.append(7)
                elif row[9]!='':
                    
                    t=[x.strip() for x in row[9].split(';')]
                    skills=skills+t
                    #print(len(skills))
                    for val in t:
                        levels.append(3)
                
                #print(skills + levels)
                if row[5]!='':
                    secondary=[x.strip() for x in row[5].split(';')]
                    m=musician(row[2], row[4],skills, levels, secondary)
                else:
                    m=musician(row[2], row[4],skills, levels)
                m_array.append(m)
            rownum+=1
            
    return(m_array)

# Used for first round of assigning
# Input: - g_array: array of groups
#        - nec_skills: array of necessary of skills for the genre
#        - musicians: array of musicians with common top genre such that
#                     musicians[skill] contains a list of musicians with skill as their primary skill
# Output: un_g_array: dictionary with skill as key and groups needing that skill as value 
# Edits: - g_array: Assigns musicians with necessary skills to groups
#        - musicians: Musicians that are assigned to groups are marked as assigned using add_musician
def assign(g_array, nec_skills, musicians):
    n = len(g_array)
    li = list(range(0,n)) + list(range(n-1,-1,-1))
    it = cycle(li)
    un_g_array = {}
    turn = 0
    for j, skill in enumerate(nec_skills):
        finished = False
        starting_turn = (turn)%n
        num_assigned = 0

        for i, m in enumerate(musicians[j]):
            turn = next(it)
            #print(turn)

            if skill in g_array[turn].skills:
                continue

            g_array[turn].add_musician(m, skill) 
            num_assigned += 1

            if num_assigned==n:
                finished = True
        
        if not finished:
           un_g_array[skill]=[x for x in g_array if skill not in x.skills]
    return un_g_array


# Used for second and third round of assigning
# Input: - un_g_array: dictionary with skill as key and groups needing that skill as value
#        - musicians: dictionary of skill as key and unassigned musicians as value
# Output: new_un_g_array: dictionary like un_g_array of groups still lacking a necessary skill
# Edits: - un_g_array: Assigns musicians with necessary skills to groups
#        - musicians: Musicians that are assigned to groups are marked as assigned using add_musician
def assign2(un_g_array, musicians):
    new_un_g_array = {}
    for skill, groups in un_g_array.items():
        n = len(groups)
        num_assigned = 0
        finished = False
        print(skill)
        for i, m in enumerate(musicians[skill]):
            print(groups)
            groups[0].add_musician(m, skill) 
            groups.pop(0)
            num_assigned += 1
            if num_assigned==n:
                finished = True
                break
        if not finished:
            new_un_g_array[skill] = groups
        
    return new_un_g_array

# Used for last round of assigning (assigning "unnecessary" ppl)
# Input: - g_array: list of geoups in a certain genre
#        - m_array: list of unassigned musicians in a certain genre (ordered by skill level)
# Output: g_array: list of groups (now with all the musicians in m_array assigned)
# Edits: - g_array: Assigns musicians with necessary skills to groups
#        - m_array: Musicians that are assigned to groups are marked as assigned using add_musician
def assign3(g_array, m_array):
    n = len(g_array)
    li = list(range(0,n)) + list(range(n-1,-1,-1))
    it = cycle(li)
    turn = 0
    for m in m_array:
        turn = next(it)
        g_array[turn].add_musician(m, m.skills)
        
    return g_array

# Combines all the different un_g_array's for each genre into a single dictionary
# Used between the second and third round of assigning
# Input: g1, g2, g3, g4: un_g_array output from assign2 function
# Output: comb_un_g_array: dictionary with skill as key and groups (from all genres) needing that skill as value
def combine(g1, g2, g3, g4):
    genre_groups = [g1, g2, g3, g4]
    comb_un_g_array = {}

    for un_g_array in genre_groups:
        for skill, groups in un_g_array.items():
            if skill not in comb_un_g_array:
                comb_un_g_array[skill] = groups
            else:
                comb_un_g_array[skill] += groups

    return comb_un_g_array


def create_necList(g_array, genre): #g_array is the list of musicians who have genre as their primary genre
            
    if genre=='Rock':
        perc=[x for x in g_array if 'Drumset/percussion' in x.skills[0]]
        singers=[x for x in g_array if 'Singer' in x.skills[0]]
        guitars=[x for x in g_array if 'Acoustic Guitar' in x.skills[0]] + [x for x in g_array if 'Electric Guitar' in x.skills[0]]
        return perc + singers + guitars
    elif genre=='Jazz':
        pass
    elif genre=='Hip-Hop/R&B':
        pass
    elif genre=='Electronic':
        num_prod=len([x for x in self.musician_array if 'Producer/beatmaker' in x.skills])
        pass
    elif genre=='Singer/Songwriter':
        pass
    pass
    
def order_bySkills(i_array, skill):#i_array is a list of musicians with skill in their skillset
    profs_for_skill=[]
    for m in i_array:
        #print(m.skills)
        s_list=m.skills
        profs=m.level
        loc=s_list.index(skill)
        #print(profs[0][loc])
    
        profs_for_skill.append(profs[0][loc])
    #result=sort_together(profs_for_skill, i_array)   
    #print(profs_for_skill)
    #return profs_for_skill
    result = [x for _,x in sorted(zip(profs_for_skill,i_array), reverse=True, key=lambda pair: pair[0])]
    return result

# Used in sort for first two rounds of assigning
# Input: - genre: e.g. 'Rock'
#        - nec_skills: list of necessary skills for genre
#        - num_groups: number of groups wanted for genre
#        - musician_array: list of all musicians
# Output: - g_array: list of groups
#         - un_g_array2: result of assign2
def sort_in_genre(genre, nec_skills, num_groups, musician_array):
    g_array = []
    for i in range(0, num_groups):
        g_array.append(group(genre, [], [])

    genre_m_array = [x for x in musician_array if genre in x.genre] # musicians with genre as top genre

    genre_skill_m_array = [] # list of lists of musicians with genre as top genre and skill as top skill
    for skill in nec_skills:
        genre_skill_m_array = genre_skill_m_array + order_bySkills([x for x in genre_m_array if genre==x.skills[0]] skill)[:num_groups]

    un_g_array = assign(g_array, nec_skills, genre_skill_m_array)

    un_g_array2 = assign2(un_g_array, make_dict(un_g_array, genre_m_array))

    return g_array, un_g_array2

def sort(musician_array):#makes all groups 
    print(len(musician_array)) 
    #Rock
    groups_rock, un_ro2=make_groups('Rock', 3, musician_array)
    #Hip-Hop
    groups_hh, un_hh2=make_groups('Hip-Hop/R&B', 3,musician_array)
    #Jazz

    #Ele
    groups_el, un_el2=make_groups('Electronic',2, musician_array)
    #Singer wasdf;lij
    groups_ss, un_ss2=make_groups('Singer/Songwriter', 3, musician_array)
    
    
    unassigned=[x for x in musician_array if x.assigned==False]
    print(len(unassigned))
    
    ''' 
    r1=group('Rock', [],[])
    r2=group('Rock', [],[])
    r3=group('Rock', [],[])

    ro=[x for x in musician_array if 'Rock' in x.genre]
    #Assign
    guitars=order_bySkills([x for x in ro if 'Electric guitar'==x.skills[0]], 'Electric guitar')
    perc=order_bySkills([x for x in ro if 'Drumset/percussion'==x.skills[0]], 'Drumset/percussion')
    singers=[x for x in ro if 'Singer'== x.skills[0]]
    singers=order_bySkills(singers, 'Singer')
    
    un_ro_array=assign([r1,r2,r3], ['Electric guitar', 'Drumset/percussion', 'Singer'], [ guitars[:3], perc[:3], singers[:3]])
    print('Rock: //////////////////////////////////////////////')
    #print(un_ro_array)
    un_ro2=assign2(un_ro_array,make_dict(un_ro_array, ro))

    #HipHop
    h1=group('Hip-Hop/R&B', [],[])
    h2=group('Hip-Hop/R&B', [],[])
    h3=group('Hip-Hop/R&B', [],[])
    h4=group('Hip-Hop/R&B', [],[])
    hh=[x for x in musician_array if 'Hip-Hop/R&B' in x.genre]
    rappers=order_bySkills([x for x in hh if 'Rapper'==x.skills[0]], 'Rapper') 
    prod=order_bySkills([x for x in hh if 'Producer/beatmaker'==x.skills[0]], 'Producer/beatmaker') 
    print(len(prod))    
    un_hh_array=assign([h1,h2,h3,h4], ['Rapper', 'Producer/beatmaker'], [rappers[:4], prod[:4]])
    print(h1)
    print(h2)
    print(h3)
    
    print(h4) 
    un_hh2=assign2(un_hh_array,make_dict(un_hh_array, hh))
    print('Hip Hop: ////////////////////////////////////////////////////////////')
    print(un_hh2)
    print(h1)
    print(h2)
    print(h3)
    print(h4) 
    #Jazz
    j1=group('Jazz', [], [])
    jazz=[x for x in musician_array if 'Jazz' in x.genre]

    #Electronic
    e1=group('Electronic', [],[])
    e2=group('Electronic', [],[])
    e3=group('Electronic', [],[])
    e4=group('Electronic', [],[])
    e5=group('Electrnoic', [],[])
    el=[x for x in musician_array if 'Electronic' in x.genre]
    el_prod=order_bySkills([x for x in musician_array if 'Producer/beatmaker'==x.skills[0]], 'Producer/beatmaker')

    un_el_array=assign([e1,e2,e3, e4, e5], ['Producer/beatmaker'], [prod[:5]])
    un_el2=assign2(un_el_array, make_dict(un_el_array, el))
    print('Electronic: ////////////////////////////////////////////')
    print(un_el_array)

    #SingerSongwriter
    ss1=group('Singer/songwriter', [],[])
    ss2=group('Singer/songwriter', [],[])
    ss3=group('Singer/songwriter', [],[])

    ss=[x for x in musician_array if 'Singer/Songwriter' in x.genre]
    singers=[x for x in ss if 'Singer'== x.skills[0]]
    singers=order_bySkills(singers, 'Singer')

    un_ss_array=assign([ss1,ss2,ss3], ['Singer'], [singers[:3]])
   
    un_ss2=assign2(un_ss_array, make_dict(un_ss_array, ss))

    print('SingerSongwriter: /////////////////////////////////')
    print(un_ss_array)
    
    unassigned=[x for x in musician_array if x.assigned==False]
    print(len(unassigned))
    print(combine(un_ro2, un_hh2,un_el2, un_ss2))
    '''
    return
def make_dict(skills, musicians):
    result={}
    for val in skills:
         result[val]=order_bySkills([x for x in musicians if val in x.skills and x.assigned ==False], val)
    return result
def make_groups(genre, num, musician_array):
    group_result=[]
    for x in range(num):
        print(x)
        group_result.append(group(genre, [],[]))
    un_2={}
    if genre == 'Rock':
        ro=[x for x in musician_array if 'Rock' in x.genre]
        guitars=order_bySkills([x for x in ro if 'Electric guitar'==x.skills[0]], 'Electric guitar')
        perc=order_bySkills([x for x in ro if 'Drumset/percussion'==x.skills[0]], 'Drumset/percussion')
        singers=[x for x in ro if 'Singer'== x.skills[0]]
        singers=order_bySkills(singers, 'Singer')
        un_array=assign(group_result, ['Electric guitar', 'Drumset/percussion', 'Singer'], [ guitars[:num], perc[:num], singers[:num]])
        un_2=assign2(un_array,make_dict(un_array, ro))
    elif genre == 'Hip Hop/R&B':
        hh=[x for x in musician_array if 'Hip-Hop/R&B' in x.genre]
        rappers=order_bySkills([x for x in hh if 'Rapper'==x.skills[0]], 'Rapper') 
        prod=order_bySkills([x for x in hh if 'Producer/beatmaker'==x.skills[0]], 'Producer/beatmaker') 
        un_array=assign(group_result, ['Rapper', 'Producer/beatmaker'], [rappers[:num], prod[:num]])
        un_2=assign2(un_array,make_dict(un_array, hh))
    elif genre=='Jazz':
        jazz=[x for x in musician_array if 'Jazz' in x.genre]
    elif genre == 'Electronic':
        el=[x for x in musician_array if 'Electronic' in x.genre]
        el_prod=order_bySkills([x for x in musician_array if 'Producer/beatmaker'==x.skills[0]], 'Producer/beatmaker')
        un_array=assign(group_result, ['Producer/beatmaker'], [el_prod[:num]])
        un_2=assign2(un_array, make_dict(un_array, el))
    elif genre=='Singer/songwriter':
        ss=[x for x in musician_array if 'Singer/Songwriter' in x.genre]
        singers=[x for x in ss if 'Singer'== x.skills[0]]
        singers=order_bySkills(singers, 'Singer')

        un_array=assign(group_result, ['Singer'], [singers[:num]])
        un_2=assign2(un_array, make_dict(un_array, ss))
    return group_result, un_2


m_array=read('entries.csv')
sort(m_array)



'''
hh=[x for x in m_array if 'Hip-Hop/R&B' in x.genre]
el=[x for x in m_array if 'Electronic' in x.genre]
jazz=[x for x in m_array if 'Jazz' in x.genre]
#for m in jazz:
#    print(m)
#for m in el:
#    print(m)

#for m in hh:
#    print(m)


ro=[x for x in m_array if 'Rock' in x.genre]
singers=[x for x in ro if 'Singer'== x.skills[0]]
singers=order_bySkills(singers, 'Singer')
#musicians=[singers]
#for m in ro:
#    print(m)
#print('Singers')
#for s in singers:
#    print(s)
perc=order_bySkills([x for x in ro if 'Drumset/percussion'==x.skills[0]], 'Drumset/percussion')
#print('Drum')
#for p in perc:
#    print(p)
guitars=order_bySkills([x for x in ro if 'Electric guitar'==x.skills[0]], 'Electric guitar')
#print('guitar')
#print(len(guitars))
#for g in guitars:
#    print(g)
g1=group('Rock', [],[])
g2=group('Rock', [],[])
g3=group('Rock', [],[])
g4=group('Rock', [], [])
#print('Assign Results')

dict_test=assign([g1,g2,g3], ['Electric guitar', 'Drumset/percussion', 'Singer'], [ guitars[:3], perc[:3], singers[:3]])
print(dict_test)
print('Before')
print('Groups')
print(g1)
print(g2)
print(g3)
m_dict=make_dict(list(dict_test.keys()), m_array)
as2=assign2(dict_test, m_dict)
print('/////////////////////////////')
print('After')
print('Groups')
print(g1)
print(g2)
print(g3)
print(as2)
#sec_drum=[x for x in ro if 'Drumset/percussion' in x.skills and x.assigned=False]
'''

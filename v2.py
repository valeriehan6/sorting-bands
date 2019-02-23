import random
import csv
import itertools
import numpy
#from more_itertools import sort_together

genre_array=['Hip-Hop/R&B', 'Rock', 'Jazz', 'Singer/Songwriter', 'Electronic']
skills_array=['Producer/beatmaker', 'Accoustic Guitar', 'Bass Guitar', 'Electric Guitar', 'Piano', 'Singer', 'Rapper', 'Drumset/percussion', 'Saxophone', 'Upright Bass', 'Trumpet', 'Trombone', 'Other']

class musician:
    def __init__(self, name,prim_genres, skills, proficiencies, sec_genres=None):
        self.name=name
        self.genre=prim_genres
        self.secondary=sec_genres
        self.skills=skills
        self.level=proficiencies
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
            print(num_perc)
            print(num_singers)
            print(num_guitars)
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
    with open(file_name) as csvDataFile:
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
    
def assign(g_array, musicians):
    #given list of group and list of people with instrument for that group, assign in ascending and descending order in order 1,2,3,3,2,1
    fb=True
    for i, m in enumerate(musicians):
        if fb:
            turn=i%3
            g_array[turn].add_musician(musicians[i], 'Singer')
            if turn==2:
                fb=False
        else:
            #print('x')
            turn=2 - i%3
            #print(turn, m)
            g_array[turn].add_musician(musicians[i], 'Singer')
            if turn==0:
                fb=True                
    return g_array
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
        print(m.skills)
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
    
def sort(musician_array):#makes all groups 
    #Rock
    ro=[x for x in musician_array if 'Rock' in x.genre]
    perc=[x for x in ro if 'Drumset/percussion' in x.skills]
    
    #HipHop
    hh=[x for x in musician_array if 'Hip-Hop/R&B' in x.genre]

    #Jazz
    jazz=[x for x in musician_array if 'Jazz' in x.genre]

    #Electronic    
    el=[x for x in musician_array if 'Electronic' in x.genre]
    
    #SingerSongwriter
    ss=[x for x in musician_array if 'Singer/Songwriter' in x.genre]
        
m_array=read('entries.csv')
ss=[x for x in m_array if 'Singer/Songwriter' in x.genre]
singers=[x for x in ss if 'Singer' in x.skills]
g1=group('Singer/Songwriter', [],[])
g2=group('Singer/Songwriter', [],[])
g3=group('Singer/Songwriter', [],[])
assign([g1,g2,g3], singers)

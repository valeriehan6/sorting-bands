import random
import csv
import itertools
import numpy

genre_array=['Hip-Hop/R&B', 'Rock', 'Jazz', 'Singer/Songwriter', 'Electronic']
skills_array=['Producer/beatmaker', 'Accoustic Guitar', 'Bass Guitar', 'Electric Guitar', 'Piano', 'Singer', 'Rapper', 'Drumset/Percussion', 'Saxophone', 'Upright Bass', 'Trumpet', 'Trombone', 'Other']
proficiency_array=['0-5', '5-10', '10-15', '15+']

class musician:
    def __init__(self, name,prim_genres, skills, proficiencies, sec_genres=None):
        self.name=name
        self.genre=prim_genres
        self.secondary=sec_genres
        self.skills=skills
        self.level=proficiencies
          
        self.ordered_skills = [x for _,x in sorted(zip(self.transform_prof(),self.skills), reverse=True)]
        #self.ordered_skills=ordered_skills
        
        self.trans_skills=self.transform_prof()
    def __str__(self):
        return repr(self)
        
    def __repr__(self):
        to_string='Name: ' + self.name
        to_string+=' |Primary Genre: '+self.genre
        if type(self.skills)==list:
            to_string+=' |Skills: ' + ', '.join(self.skills)
            to_string+=' |Proficiencies: ' + ', '.join(self.level)
        else:
            to_string+=' |Skills: ' + self.skills
            to_string+=' |Profficiences: ' + self.level
        if self.secondary != None:
            if type(self.secondary)==list:
                to_string+=' |Secondary Genres: ' + ', '.join(self.secondary)
            else:
                to_string+=' |Seondary Genres: ' + self.secondary
        return to_string
    def transform_prof(self):
        nums=list()
        for p in self.level:
            if p=='0-5':
                nums.append(1)
            elif p=='5-10':
                nums.append(3)
            elif p=='10-15':
                nums.append(5)
            elif p=='15+':
                nums.append(7)
        return nums
            
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
            
            profs.append((m.transform_prof()[loc]))
        return(numpy.mean(profs))
            
    def checkComplete(self):
        
        self.iscomplete=False
        '''
        if (self.genre=='Hip-Hop/R&B'):
            if ('Producer/beatmaker' in self.skills and 'Rapper' in self.skills):
                self.iscomplete=True  
        elif (self.genre=='Rock'):######################
            if(('Drumset/Percussion' in self.skills or 'Producer/beatmaker' in self.skills) and 'Singer' in self.skills):
                if(('Accoustic Guitar' in self.skills or 'Electric Guitar' in self.skills or 'Accoustic Guitar' in self.skills) and 'Bass Guitar' in self.skills):
                    self.iscomplete=True
            #etc....
        elif (self.genre=='Jazz'):##########################
            if('Saxophone' in self.skills or 'Trumpet' in self.skills or 'Trombone' in self.skills):
                if('Drumset/Percussion' in self.skills):
                    if('Upright Bass' in self.skills or 'Bass Guitar' in self.skills):
                        self.iscomplete=True
            #etc...
        elif (self.genre=='Singer/Songwriter'):########################
            if('Singer' in self.skills and len(self.musician_array)>=2):
                self.iscomplete=True
        elif(self.genre=='Electronic'):
            if('Producer/beatmaker' in self.skills):
                self.iscomplete=True
        
        '''
        num_rappers=len([x for x in self.musician_array if 'Rapper' in x.skills])
        num_prod=len([x for x in self.musician_array if 'Producer/beatmaker' in x.skills])
        num_perc=len([x for x in self.musician_array if 'Drumset/percussion' in x.skills])
        num_singers=len([x for x in self.musician_array if 'Singer' in x.skills])
        num_guitars=len([x for x in self.musician_array if 'Acoustic Guitar' in x.skills]) + len([x for x in self.musician_array if 'Electric guitar' in x.skills])
        num_bassG=len([x for x in self.musician_array if 'Bass guitar' in x.skills])
        
        
        #self.iscomplete=False
        
        if (self.genre=='Hip-Hop/R&B'):
            if (num_prod>=1 and num_rappers >=1):
                self.iscomplete=True  
        elif (self.genre=='Rock'):######################
            #print('x')
            #print(num_perc, num_singers, num_guitars)
            if ((num_perc>=1) and num_singers>=1 and num_guitars>=1):
                #print('x')
                #if(num_guitars>=1 or num_bassG >=1):
                self.iscomplete=True
            #etc....
        elif (self.genre=='Jazz'):##########################
            num_horn=len([x for x in self.musician_array if 'Saxophone' in x.skills]) + len([x for x in self.musician_array if 'Trumpet' in x.skills]) + len([x for x in self.musician_array if 'Trombone' in x.skills])
            num_dBass=len([x for x in self.musician_array if 'Upright Bass' in x.skills])
            if (num_perc>=1 and num_horn>=1 and (num_dBass>=1 or num_bassG>=1)):
                self.iscomplete=True
            #etc...
        elif (self.genre=='Singer/Songwriter'):########################
            if(num_singers>=1 and len(self.musician_array)>=2):
                self.iscomplete=True
        elif(self.genre=='Electronic'):
            if(num_prod>=1):
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
def match(musician_array):
    #groups=list()
    #divide into genres
    #hh=[x for x in musician_array if 'Hip-Hop/R&B' in x.genre]
    jazz=[x for x in musician_array if 'Jazz' in x.genre]
    #el=[x for x in musician_array if 'Electronic' in x.genre]
    #ro=[x for x in musician_array if 'Rock' in x.genre]
    #ss=[x for x in musician_array if 'Singer/Songwriter' in x.genre]
    
    #hh_groups=group_combos('Hip-Hop/R&B', hh)
    jazz_groups=group_combos('Jazz', jazz)
    #el_groups=group_combos('Electronic', el)
    #ro_groups=group_combos('Rock', ro)
    #ss_groups=group_combos('Singer/Songwriter', ss)
    
    prof_avg=get_totalavg(jazz_groups) 
    
    groupings=get_groupings(jazz_groups)
    optimal_hhgroups=get_best_groups(groupings,prof_avg)
    #repeat for genres
    
    return groupings[optimal_hhgroups]
            
def group_combos(genre, musicians):
    
    combos=list(itertools.combinations(musicians,4)) + list(itertools.combinations(musicians,5))
    groups=list()
    for c in combos:
        #print(c)
        new_group=group(genre, c, [x.ordered_skills[0] for x in c])
        if new_group.checkComplete():
            groups.append(new_group)
    return groups

def check_unique(grouping):
    musicians=list()
    for g in grouping:
            for m in g.musician_array:
                if m in musicians:
                    return False
                else:
                    musicians.append(m)
    return True

def get_groupings(list_of_groups):
    groupings=list(itertools.combinations(list_of_groups,1))+list(itertools.combinations(list_of_groups, 2))# + list(itertools.combinations(list_of_groups,3))
    #result=groupings
    unique_groupings=[x for x in groupings if check_unique(x)==True]
    return unique_groupings
def get_totalavg(list_of_groups):
    running_avg=0
    for g in list_of_groups:
        running_avg+=g.get_avgprofs()
    return running_avg/len(list_of_groups)
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
                    for i in range(len(t)):
                        levels.append('15+')
                if row[11]!='':
                    t=[x.strip() for x in row[11].split(';')]
                    skills=skills+t
                    for i in range(len(t)):
                        levels.append('10-15')
                if row[10]!='':
                    t=[x.strip() for x in row[10].split(';')]
                    skills=skills+t
                    for i in range(len(t)):
                        levels.append('5-10')
                elif row[9]!='':
                    t=[x.strip() for x in row[9].split(';')]
                    skills=skills+t
                    for i in range(len(t)):
                        levels.append('0-5')
                
                #print(skills + levels)
                if row[5]!='':
                    secondary=[x.strip() for x in row[5].split(';')]
                    m=musician(row[2], row[4],skills, levels, secondary)
                else:
                    m=musician(row[2], row[4],skills, levels)
                m_array.append(m)
            rownum+=1
            
    return(m_array)
            
def get_best_groups(grouping_options, avg):
    best_dist=9999
    best_dist_loc=0
    max_ppl=0
    #max_ppl_loc
    for index, go in enumerate(grouping_options):
        if type(go)!=list or len(go)==1:
            #print(go)
            g=go[0]
            group_avg=g.get_avgprofs()
            if numpy.absolute(group_avg-avg)<best_dist:
                print('0')
                best_dist=numpy.absolute(group_avg-avg)
                best_dist_loc=index
            if ((numpy.absolute(group_avg-avg)<best_dist+100 or numpy.absolute(group_avg-avg)>best_dist-100) and len(g.musician_array)>len(grouping_options[best_dist_loc][0].musician_array)):
                print('0')
                best_dist=numpy.absolute(group_avg-avg)
                best_dist_loc=index
                
        else:
            running_dist=0
            num_musicians=0
            for g in go:
                num_musicians+=len(g[0].musician_array)
                running_dist+=numpy.absolute(g[0].get_avgprofs()-avg)
            if(running_dist<best_dist):
                best_dist=running_dist
                best_dist_loc=index
                max_ppl=num_musicians
            if((running_dist<best_dist+1 or running_dist>best_dist-1)):
                if(num_musicians>max_ppl):
                    best_dist=running_dist
                    best_dist_loc=index
                    max_ppl=num_musicians
    return best_dist_loc

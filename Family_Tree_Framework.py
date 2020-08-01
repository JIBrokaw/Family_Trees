#format needed for data input: ['Name', [nicknames], 'year', [Bigs], [family founded], [other data]]

#import Kwah_record.csv
from collections import deque
import csv

class Family:
    class __Member:
        def __init__(self, name, year, families, other_data):
            self.__name = name
            self.__year = year
            self.__legacy = 0
            self.__heritage = 0
            self.__twins = []
            self.__families = families
            self.__other_data = other_data

        def get_name(self):
            return self.__name

        def get_grade(self):
            return self.__year

        def get_height(self):
            return self.__legacy

        def get_depth(self):
            return self.__heritage

        def update_height(self,addition):
            self.__legacy = addition + 1

        def update_depth(self,addition):
            self.__heritage = addition + 1

        def get_twins(self):
            return self.__twins

        def update_twins(self, member):
            self.__twins.append(member)

        def get_other_data(self):
            return self.__other_data

        def update_families(self,family):
            if family in self.__families:
                if family.startswith('NOT'):
                    self.__families.remove(family)
            else:
                if "NOT " + family not in self.__families:
                    self.__families.append(family)

        def get_families(self):
            return self.__families


    def __init__(self):
        self.__member_list = dict()
        self.__full_name_lookup = dict()
        self.__adjacent_Bigs = dict()
        self.__adjacent_Littles = dict()

    def get_Big_List(self):
        return self.__adjacent_Bigs

    def get_Little_List(self):
        return self.__adjacent_Littles

    #Updates the number of descended generations when a new little is added
    def __update_legacy(self, member):
        for i in self.__adjacent_Bigs[member]:
            stop = False
            for j in self.__adjacent_Littles[i]:
                if j.get_height() > member.get_height():
                    stop = True
                    break
            if stop == False:
                i.update_height(member.get_height())
                self.__update_legacy(i)
    def __update_heritage(self, member):
        for Big in self.__adjacent_Bigs[member]:
            if Big.get_depth() >= member.get_depth():
                member.update_depth(Big.get_depth())


    #Hasher to find right key-name from possible inputs.
    def __find_real_name(self, name, altName = ''):
        try:
            key = self.__full_name_lookup[name]
            if len(key) > 1:
                if altName == '':
                    answer = input('Please specify which ' + name.title() + ' you mean.' + '\n\t' + '\n\t'.join(i.title() for i in key) + '\n').lower()
                else:
                    answer = altName
                if answer not in key:
                    if ' ' in answer:
                        temp = answer.split()
                        answer = temp[(len(temp)-1)]
                    for i in key:
                        if answer in i:
                            return i.rstrip("1234567890() ")
                return answer.rstrip("1234567890() ")
            else:
                return key[0].rstrip("1234567890() ")
        except:
            if ' ' in name:
                name = name.split()
                return self.__find_real_name(name[0], name[len(name)-1])
            else:
                raise KeyError

    #Public function, input name and returns Member object
    def find_member(self, Name):
        name = Name.lower()
        try:
            if " " in name:
                return self.__member_list[name]
            else:
                raise KeyError
        except:
            real_name = self.__find_real_name(name)
            return self.find_member(real_name)

    #Public function, input member's data and link to structure.
    def add_new_member(self, name, nicknames, year, Bigs, families, other_data):
        if type(Bigs) != list:
            Bigs = [Bigs]
        if type(nicknames) != list:
            nicknames = [nicknames]
        if type(families) != list:
            families = [families]

        for big in Bigs:
            if big.lower() not in self.__member_list:
                raise KeyError

        for i in range(len(Bigs)):
            Bigs[i] = self.__member_list[Bigs[i].lower()]

        #create member and add names to rosters
        member = self.__Member(name, year, families, other_data)
        self.__member_list[name.lower()] = member
        name_words = name.split()
        for i in name_words:
            if len(member.get_grade()) > 4:
                grade = member.get_grade().strip('abcdefghijklmnopqrstuvwxyz() ')
                grade = grade[:4]
            else:
                grade = member.get_grade()
            try:
                self.__full_name_lookup[i.lower()].append(member.get_name().lower() + " (" + grade + ")")
            except:
                self.__full_name_lookup[i.lower()] = [member.get_name().lower() + " (" + grade + ")"]
        for i in nicknames:
            try:
                self.__full_name_lookup[i.lower()].append(member.get_name().lower() + " (" + grade + ")")
            except:
                self.__full_name_lookup[i.lower()] = [member.get_name().lower() + " (" + grade + ")"]
        #link member in with family
        self.__adjacent_Littles[member] = []
        self.__adjacent_Bigs[member] = Bigs
        for i in Bigs:
            for k in self.__adjacent_Littles[i]:
                if k not in member.get_twins():
                    if self.__adjacent_Bigs[k] == Bigs:
                        k.update_twins(member)
                        member.update_twins(k)
            self.__adjacent_Littles[i].append(member)
            for j in i.get_families():
                member.update_families(j)
        #remove families
        pointer = 0
        while pointer < len(member.get_families()):
            if member.get_families()[pointer].startswith('NOT'):
                member.update_families(member.get_families()[pointer])
            else:
                pointer += 1

        #record height
        self.__update_heritage(member)
        self.__update_legacy(member)

    #Given a member, returns a properly-formatted string explaining their Bigs and full-siblings
    def __describe_Bigs(self,member):
        Bigs = self.__adjacent_Bigs[member]
        #Twins = []
        if len(Bigs) > 0:
            # for i in range(len(Bigs)):
            #     for j in range(len(self.__adjacent_Littles[Bigs[i]])):
            #         sib = self.__adjacent_Littles[Bigs[i]][j]
            #         if sib != member and self.__adjacent_Bigs[sib] == Bigs and sib not in Twins:
            #             Twins.append(sib)
            if len(member.get_twins()) == 0:
                return ' and '.join(i.get_name() for i in Bigs) + " begat " + member.get_name() + '.'
            else:
                return ' and '.join(i.get_name() for i in Bigs) + " begat " + member.get_name() + ''.join((', ' + member.get_twins()[i].get_name()) for i in range(len(member.get_twins())-1)) + ' and ' + member.get_twins()[len(member.get_twins())-1].get_name() + "."
        else:
            return ''

    #Given a member, returns a properly-formatted string explaining their Littles and co-bigs
    def __describe_Littles(self,member):
        Littles = self.__adjacent_Littles[member]
        string_solo = None
        string_co = None
        coParented = []
        if len(Littles) > 0:
            for i in range(len(Littles)):
                if len(self.__adjacent_Bigs[Littles[i]]) >1 :
                    coParented.append(Littles[i])
            for i in range(len(coParented)):
                match = False
                for j in range(i+1,len(coParented)):
                    if self.__adjacent_Bigs[coParented[j]] == self.__adjacent_Bigs[coParented[i]]:
                        match = True
                if not match:
                    if string_co is not None:
                        if type(string_co) is str:
                            string_co = [string_co]
                        string_co = string_co + [self.__describe_Bigs(coParented[i])]
                        #string_co = string_co + "\n\t" + self.__describe_Bigs(coParented[i])
                    else:
                        string_co = self.__describe_Bigs(coParented[i])

            solo_littles = [i for i in Littles if i not in coParented]
            if len(solo_littles) > 0:
                if len(solo_littles) == 1:
                    string_solo = member.get_name() + ' begat ' + solo_littles[0].get_name() + '.'
                else:
                    string_solo = member.get_name() + ' begat ' + ', '.join(solo_littles[i].get_name() for i in range(len(solo_littles)-1)) + ' and ' + solo_littles[len(solo_littles)-1].get_name() + '.'
            return [string_solo, string_co]
        else:
            return [None,None]

    #Public Function. Given a member, returns a list of their total siblings
    def get_siblings(self,member):
        Bigs = self.__adjacent_Bigs[member]
        Siblings = []
        for i in Bigs:
            for j in self.__adjacent_Littles[i]:
                if j is not member and j not in Siblings:
                    Siblings.append(j)
        return Siblings

    #Public Function. Given a member, returns a list of their coBigs
    def get_coBigs(self,member):
        Littles = self.__adjacent_Littles[member]
        coBigs = []
        for i in Littles:
            for j in self.__adjacent_Bigs[i]:
                if j is not member and j not in coBigs:
                    coBigs.append(j)
        return coBigs


    #TRAVERSAL METHODS
        #Loops through all Bigs until someone has no Big listed. Updates the Stack of members in place
    def __Big_trail(self,member,Ancestors):
        Bigs = self.__adjacent_Bigs[member]
        for i in range(len(Bigs)):
            Ancestors.append(Bigs[i])
            self.__Big_trail(Bigs[i],Ancestors)

        #Loops through all Littles until someone has no Little listed. Updates the Queue of members in place
    def __Little_trail(self,member,Descendants,depth):
        Littles = self.__adjacent_Littles[member]
        # for i in range(1,len(Littles)):
        #     subtrahend = 1
        #     while Littles[i-subtrahend].get_height() > Littles[i].get_height():
        #         temporary = Littles[i-subtrahend]
        #         Littles[i-1] = Littles[i]
        #         Littles[i] = temporary
        #         subtrahend -= 1
        for i in range(len(Littles)):
            # if 0< i < len(Littles):
            #     if Littles[i].get_height() > 1:
            #             Descendants.append(' ')
            Descendants.append([Littles[i], depth])
            self.__Little_trail(Littles[i], Descendants, depth + 1)

        #Returns the results of Big_trail() without duplicates
    def __get_heritage(self,member):
        Bigs = self.__adjacent_Bigs[member]
        Ancestors = deque()
        self.__Big_trail(member,Ancestors)
        #count = 0
        generations = [None]*len(Ancestors)
        for i in range(len(Ancestors)):
            person = Ancestors.pop()
            if person not in generations:
                for twin in person.get_twins():
                    if twin in generations:
                        #print(person.get_name() + ' ' + twin.get_name())
                        break
                generations[i] = person
                #count +=1
                Ancestors.appendleft(person)
        return Ancestors
        # reduced_generations = [None]*count
        # for i in range(count):
        #     reduced_generations[i] = generations[i]
        # return reduced_generations

        #Returns the results of Little_trail() without duplicates
    def __get_legacy(self,member):
        Littles = self.__adjacent_Littles[member]
        Descendants = deque()
        self.__Little_trail(member, Descendants, 0)
        #count = 0
        Generations = [None]*len(Descendants)
        for i in range(len(Descendants)):
            person_data = Descendants.popleft()
            if person_data[0] not in Generations:
                Generations[i] = person_data[0]
                Descendants.append(person_data)
        return Descendants
        # generations = [None]*len(Descendants)
        # for i in range(len(Descendants)):
        #     person_data = Descendants.popleft()
        #     duplicate = False
        #     for i in range(count):
        #         if person_data[0] == generations[i][0]:
        #             duplicate = True
        #             break
        #     if duplicate == False:
        #         generations[count] = person_data
        #         count +=1
        # reduced_generations = [None]*count
        # for i in range(count):
        #     reduced_generations[i] = generations[i]
        # return reduced_generations

        #Joins the results of __get_legacy() and __get_heritage() into a string. Returns the properly formatted string.
    def get_lineage(self,member):
        past = self.__get_heritage(member)
        future = self.__get_legacy(member) #a deque of 2-value arrays, member/depth

        statements = ['']*(len(past)+len(future)*2+4)
        count = 0

        for i in range(len(past)):
            person_i = past.pop()
            statements[i] = '  '*person_i.get_depth() + (self.__describe_Bigs(person_i))
            count += 1
        if(len(self.__adjacent_Bigs[member]) > 0):
            statements[count] = '--'*(member.get_depth() - 1) + '> '+ (self.__describe_Bigs(member))
        member_data = self.__describe_Littles(member)
        if member_data[0] is not None:
            statements[count + 1] = '  '*(member.get_depth() +1) + member_data[0]
        if type(member_data[1]) is str:
            statements[count + 2] = '  '*(member.get_depth() +1) + member_data[1]
        elif member_data[1] is not None:
            for i in range(len(member_data[1])):
                statements[count + 2] = '  '*(member.get_depth() +1) + member_data[1][i]
                count += 1
        for i in range(len(future)):
            person_data = future.popleft()
            #print(person_data[0].get_name())
            little_descriptions = self.__describe_Littles(person_data[0])
            for j in range(2):
                if little_descriptions[j] is None:
                    pass
                elif j == 0 or type(little_descriptions[1]) is str:
                    phrase = '  '*(person_data[1] + member.get_depth() + 2) + little_descriptions[j]
                    if not phrase.isspace() and phrase != '':
                        statements[count + 3] = phrase
                        count += 1
                else:
                    for k in range(len(little_descriptions[1])):
                        statements[count + 3] = '  '*(person_data[1] + member.get_depth() + 2) + little_descriptions[j][k]
                        count += 1
            # for j in range(2):
            #     try:
            #         phrase = '  '*(future[i].get_depth() + 1) + self.__describe_Littles(future[i])[j]
            #     except TypeError:
            #         print('type')
            #         if statements[count + 2] == ' ':
            #             break
            #         phrase = ' '
            #     if not phrase.isspace() and phrase is not None and phrase.lstrip() not in (statements[i].lstrip() for i in range(count +2)):
            #         statements[count + 3] = phrase
            #         count += 1

        for i in range(len(statements)):
            for j in range(i + 1, len(statements)):
                if statements[i].strip() == statements[j].strip():
                    statements[j] = ''
        return('\n'.join("\t" + i for i in statements if i != '' and i is not None))

#Converts the input record data into a family structure.
def setup_family(record,year,expected_len):
    family_name = Family()
    year = year
    premature = deque()
    with open(record,'r') as file:
        file.readline()
        for line in file:
            if line.startswith(',') or line.startswith('20') or line.startswith('19'):
                for i in range(len(premature)):
                    trial = premature.popleft()
                    try:
                        family_name.add_new_member(trial[0],trial[1],trial[2],trial[3],trial[4],[trial[i] for i in range(5, len(trial))])
                    except:
                        premature.append(trial)
            else:
                start_pointer = 0
                listing = False
                person = []
                sublist = []
                for end_pointer in range(len(line)):
                    if line[end_pointer] == '"':
                        if listing == False:
                            listing = True
                            start_pointer = end_pointer + 1
                            sublist = []
                        else:
                            listing = False
                            sublist.append(line[start_pointer:end_pointer])
                            person.append(sublist)
                            start_pointer = end_pointer + 2
                    elif line[end_pointer] == ',':
                        if listing == False:
                            if line[end_pointer-1] != '"':
                                if start_pointer == end_pointer:
                                    person.append([])
                                else:
                                    person.append(line[start_pointer:end_pointer])
                        else:
                            sublist.append(line[start_pointer:end_pointer])
                        start_pointer = end_pointer+1
                        while line[start_pointer] == ' ':
                            start_pointer += 1
                if line[len(line)-2] == ',':
                    person.append('')
                elif line[len(line)-2] != '"':
                    person.append(line[start_pointer:len(line)-1])
                try:
                    if len(person) < expected_len:
                        print('short' + person[0])
                    if len(person) > expected_len:
                        print('long' + person[0])
                    if len(person) == expected_len:
                        family_name.add_new_member(person[0],person[1],person[2],person[3],person[4], [person[j] for j in range(5, len(person))])
                except:
                    premature.append(person)
            year += 1
    if len(premature) > 0:
        print(premature)
        raise KeyError
    return family_name

def print_roster(year, record, intro_string, dataKey):
    print('\n' + intro_string + str(year) + '\n')
    with open(record, 'r', newline = '') as file:
        reader = csv.reader(file)
        in_year = False
        for row in reader:
            if row[0] == str(year):
                in_year = True
            if in_year and row[2] != '':
                additional_data = ' (' + row[dataKey] + ')'
                year_bonus = ''
                if not row[2].endswith(str(year)):
                    if 'w' in row[2]:
                        if not row[2].startswith('('):
                            year_bonus = ' (graduated ' + (row[2].split()[0]) + ')'
                    else:
                        year_bonus = ' ' + ' '.join(row[2].split()[j] for j in range(1,3))
                print('\t' + row[0] + additional_data + year_bonus)
            if row[0] == str(year+1):
                break

if __name__ == "__main__":
    pass

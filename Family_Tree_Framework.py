#format needed for data input: ['Name', [nicknames], 'year', [Bigs], [family founded], [other data]]


from collections import deque

class Family:
    class __Member:
        def __init__(self, name, year, families, other_data):
            self.__name = name
            self.__year = year
            self.__families = families
            self.__other_data = other_data

        def get_name(self):
            return self.__name

        def get_grade(self):
            return self.__year

        def get_other_data(self):
            return self.__other_data

        def update_families(self,family):
            if family not in self.__families:
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
                            return i
                return answer
            else:
                return key[0]
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
            return self.__member_list[name]
        except:
            real_name = self.__find_real_name(name)
            return self.find_member(real_name)

    #Public function, input member's data and link to structure.
    def add_new_member(self, name, nicknames, year, Big_names, families, other_data):
        Bigs = []
        for i in range(len(Big_names)):
            Bigs.append(self.find_member(Big_names[i]))
        #create member and add names to rosters
        member = self.__Member(name, year, families, other_data)
        self.__member_list[member.get_name().lower()] = member
        for i in nicknames:
            try:
                self.__full_name_lookup[i.lower()].append(member.get_name().lower())
            except:
                self.__full_name_lookup[i.lower()] = [member.get_name().lower()]
        #link member in with family
        self.__adjacent_Littles[member] = []
        self.__adjacent_Bigs[member] = Bigs
        for i in Bigs:
            self.__adjacent_Littles[i].append(member)
            for j in i.get_families():
                #print(name + ' ' + i.get_name() + ' ' + j)
                member.update_families(j)

    #Given a member, returns a properly-formatted string explaining their Bigs and full-siblings
    def __describe_Bigs(self,member):
        Bigs = self.__adjacent_Bigs[member]
        Twins = []
        if len(Bigs) > 0:
            for i in range(len(Bigs)):
                for j in range(len(self.__adjacent_Littles[Bigs[i]])):
                    sib = self.__adjacent_Littles[Bigs[i]][j]
                    if sib != member and self.__adjacent_Bigs[sib] == Bigs and sib not in Twins:
                        Twins.append(sib)
            return ' and '.join(i.get_name() for i in Bigs) + " begat " + member.get_name() + ''.join((' and ' + i.get_name()) for i in Twins) + "."
        else:
            return ''

    #Given a member, returns a properly-formatted string explaining their Littles and co-bigs
    def __describe_Littles(self,member):
        Littles = self.__adjacent_Littles[member]
        string_one = ''
        string_two = ''
        coParented = []
        if len(Littles) > 0:
            for i in range(len(Littles)):
                if self.__adjacent_Bigs[Littles[i]] != [member]:
                    coParented.append(Littles[i])
            for i in coParented:
                string_two = self.__describe_Bigs(i)
            solo_littles = [i for i in Littles if i not in coParented]
            if len(solo_littles) > 0:
                string_one = member.get_name() + ' begat ' + ' and '.join(i.get_name() for i in solo_littles)
            return [string_one, string_two]
        else:
            return ['','']

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
        #Loops through all Bigs until someone has no Big listed. Updates the Stack in place
    def __Big_trail(self,member,Ancestors):
        Bigs = self.__adjacent_Bigs[member]
        for i in range(len(Bigs)):
            Ancestors.append(Bigs[i])
            self.__Big_trail(Bigs[i],Ancestors)

        #Loops through all Littles until someone has no Little listed. Updates the Queue in place
    def __Little_trail(self,member,Descendants):
        Littles = self.__adjacent_Littles[member]
        for i in range(len(Littles)):
            Descendants.append(Littles[i])
            self.__Little_trail(Littles[i],Descendants)

        #Returns the results of Big_trail() without duplicates
    def __get_heritage(self,member):
        Bigs = self.__adjacent_Bigs[member]
        Ancestors = deque()
        self.__Big_trail(member,Ancestors)
        count = 0
        generations = [None]*len(Ancestors)
        for i in range(len(Ancestors)):
            person = Ancestors.pop()
            if person not in generations:
                generations[count] = person
                count +=1
        reduced_generations = [None]*count
        for i in range(count):
            reduced_generations[i] = generations[i]
        return reduced_generations

        #Returns the results of Little_trail() without duplicates
    def __get_legacy(self,member):
        Littles = self.__adjacent_Littles[member]
        Descendants = deque()
        self.__Little_trail(member,Descendants)
        count = 0
        generations = [None]*len(Descendants)
        for i in range(len(Descendants)):
            person = Descendants.popleft()
            if person not in generations:
                generations[count] = person
                count +=1
        reduced_generations = [None]*count
        for i in range(count):
            reduced_generations[i] = generations[i]
        return reduced_generations

        #Joins the results of __get_legacy() and __get_heritage() into a string. Returns the properly formatted string.
    def get_lineage(self,member):
        past = self.__get_heritage(member)
        future = self.__get_legacy(member)

        statements = [None]*(len(past)+len(future)*2+4)
        count = 0

        for i in range(len(past)):
            statements[i] = (self.__describe_Bigs(past[i]))
            count += 1

        statements[count] = (self.__describe_Bigs(member))
        statements[count + 1] = self.__describe_Littles(member)[0]
        statements[count + 2] = self.__describe_Littles(member)[1]

        for i in range(len(future)):
            for j in range(2):
                phrase = self.__describe_Littles(future[i])[j]
                if phrase not in statements:
                    statements[count + 3] = phrase
                    count += 1

        return('\n'.join("\t" + i for i in statements if i != '' and i is not None))

#Converts the input record data into a family structure.
def setup_family(record,year,expected_len):
    family_name = Family()
    year = year
    premature = deque()
    while year in record:
        for i in range(len(premature)):
            trial = premature.popleft()
            try:
                family_name.add_new_member(trial[0],trial[1],trial[2],trial[3],trial[4],[trial[i] for i in range(5, expected_len)])
            except:
                premature.append(trial)

        for i in record[year]:
            try:
                if len(i) < expected_len:
                    print('short' + i[0])
                if len(i) > expected_len:
                    print('long' + i[0])
                if len(i) == expected_len:
                    family_name.add_new_member(i[0],i[1],i[2],i[3],i[4], [i[j] for j in range(5, expected_len)])
            except:
                premature.append(i)
        year += 1
    if len(premature) > 0:
        print(premature)
        raise KeyError
    return family_name

#prints the input year's list of students, properly formatted
def print_roster(year, record, intro_string, dataKey):
    print('\n' + intro_string + str(year) + '\n')
    for i in record[year]:
        additional_data = ' (' + i[dataKey] + ')'
        year_bonus = ''
        if not i[2].endswith(str(year)):
            if 'w' in i[2]:
                year_bonus = ' (graduated ' + (i[2].split()[0]) + ')'
            else:
                year_bonus = ' ' + ' '.join(i[2].split()[j] for j in range(1,3))
        print('\t' + i[0] + additional_data + year_bonus)


if __name__ == "__main__":
    pass

#Desired features:
#From one member, can identify all close relatives: Bigs, Littles, ancestors, descendants, siblings. Marriages? COMPLETE
#Cobigging and twins are allowed, as are both at once. COMPLETE


#Optional features:
#Students are sorted by entering grad year. COMPLETE
#Click on a name and highlight relatives throughout the list with different colors depending on relationship.OBSOLETE
#(Search methods not really necessary if sorted by grad year, but might be nice?) COMPLETE

#Features needed temporarily:
#Ability to add more ancestors backwards as I discover old family lines.

#Eventual features needed:
#Can append a new generation of kwahlings to the tree, linking them in with their Bigs.
#(No backwards addition of ancestors required.)
#(Also once data is in, no mutation required. Except maybe an undo operation.)
#Interface for non-CS major to add new generation.
#Visual representation of tree centered at chosen individual


from Sample_Family_Record import People
import Family_Tree_Framework

def get_data(family, member):
    voice = member.get_other_data()[0]

    coBigs = family.get_coBigs(member)
    coString = ''
    if len(coBigs) > 0:
        coString = '\nCo-Big(s): ' + 'and'.join(i.get_name() for i in coBigs)

    sibs = family.get_siblings(member)
    sibString = ''
    if len(sibs) > 0:
        sibString = '\nSibling(s): ' + ' and '.join(i.get_name() for i in sibs)
        # if len(member.get_twins()) > 0:
        #     sibString = sibString + '\tTwin(s): ' + ' and '.join(i.get_name() for i in member.get_twins())

    fandom = member.get_other_data()[0]
    fandomstring = ''
    if len(fandom) > 0:
        fandomstring = '\n\tFandom Affiliation: ' + '\n\t\t\t   '.join(i for i in fandom)


    string = member.get_name() + ':\n\tClass: ' + str(member.get_grade()) + fandomstring + '\n\nBig(s): ' + ' and '.join(i.get_name() for i in family.get_Big_List()[member]) + '\nLittle(s): ' + ' and '.join(i.get_name() for i in family.get_Little_List()[member]) + coString + sibString + '\nFamily: ' + ' and '.join(i for i in member.get_families() if i != '')
    string = string + "\nGenerations Descended: " + str(member.get_height())# + '\nGenerations before: ' + str(member.get_depth())
    return string


if __name__ == "__main__":
    start_year = 2019
    #my_fam = Family_Tree_Framework.setup_family(Kwahlings,start_year,7)
    my_fam = Family_Tree_Framework.setup_family(People,start_year,6)
    print("\nWelcome to the History of the Organization. \n\tEnter a member's name to learn their lineage. \n\tEnter a graduation year to get the roster of that social class. \n\tType 'exit' to quit.")
    while True:
        person = input('\nWhat would you like to know? ').lower()
        if person == 'exit':
            break
        try:
            year = int(person)
            Family_Tree_Framework.print_roster(year, People, 'The Organization members of the class of ', 5)
        except ValueError:
            try:
                person = my_fam.find_member(person)
                print('\n' + get_data(my_fam, person) + '\n')
                print('The tale of generations:')
                print(my_fam.get_lineage(person))
            except KeyError:
                #except KeyError:
                print('That name is not recognized. Please try again.')
        except KeyError:
            print("Unfortunately, that year is not yet included in this database.")

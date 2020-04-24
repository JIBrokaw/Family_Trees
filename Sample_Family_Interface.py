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

    officer = member.get_other_data()[1]
    offistring = ''
    if len(officer) > 0:
        offistring = '\nOfficer Positions: ' + '\n\t\t   '.join(i for i in officer)

    string = member.get_name() + ':\n\tClass: ' + str(member.get_grade()) + '\n\tVoice Part: ' + voice + '\n\nBig(s): ' + ' and '.join(i.get_name() for i in family.get_Big_List()[member]) + '\nLittle(s): ' + ' and '.join(i.get_name() for i in family.get_Little_List()[member]) + coString + sibString + '\nKwah Family: ' + ' and '.join(i for i in member.get_families()) + offistring
    return string



if __name__ == "__main__":
    my_fam = Family_Tree_Framework.setup_family(People,2014,7)
    print("\nWelcome to the History of the Organization. \n\tEnter an organization member's name to learn their lineage. \n\tEnter a graduation year to get the roster of that social class. \n\tType 'exit' to quit.")
    while True:
        person = input('\nWhat would you like to know? ').lower()
        if person == 'exit':
            break
        try:
            year = int(person)
            Family_Tree_Framework.print_roster(year, People, 'The members of the class of ', 5)
        except ValueError:
            try:
                person = my_fam.find_member(person)
                print('\n' + get_data(my_fam, person) + '\n')
                print('The tale of generations:')
                print(my_fam.get_lineage(person))
            except KeyError:
                print('That name is not recognized. Please try again.')
        except KeyError:
            print("Unfortunately, that year is not yet included in this database.")

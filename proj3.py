
from person import Person
import json

class DynasticDescent:

    def __init__(self):

        self.family_tree = {} #key is the name, value is the object


    def add_person(self, person_name):
        """
        :param person_name: string
        :return: None
        """
        #this will check if the object is in the tree and if it isn't then it will add.
        person_exist = False
        for person in self.family_tree:
            if person == person_name:
                print("This person already exists in the dictionary")
                person_exist = True

        if person_exist == False:
            self.family_tree[person_name] = Person(person_name)

    def find_children(self, curr_person, degree):
        """
        :param curr_person: current children
        :param degree: the descendants number
        :return: child name
        """
        child_list_object = curr_person.child_list

        #base case
        if degree == 0:
            return curr_person
        if degree == 1:
            return child_list_object
        else:
            child_descendants = []
            #iterates through the child object and finds the child at the index. degree is subtracted for recursive case
            for i in range(len(child_list_object)):
                child_generation = self.find_children(child_list_object[i], degree - 1)
                for j in child_generation:
                    child_descendants.append(j)
            return child_descendants


    def find_parents(self, curr_person, degree):
        """
        :param curr_person: current person (string)
        :param degree: the degree for the recursive parents
        :return: parents
        """

        #base case
        if degree == 0:
            return curr_person
        elif degree == 1:
            return curr_person.get_parent()

        parent_list_object = curr_person.get_parent()

        actual_parents = []

        #finds the parent in the objects
        for j in parent_list_object:
            parents = self.find_parents(j, degree - 1)
            for i in parents:
                actual_parents.append(i)

        return actual_parents

    def get_siblings(self, person_name):
        """
        :param person_name: string to get the siblings
        :return: list of siblings
        """
        #iterates through the parent list and then finds the children who have the same parent. checks for their names and appends to actual sibling.
        actual_sibling = []
        person_object = self.family_tree[person_name]
        parent_list = person_object.get_parent()
        for parent in parent_list:
            potential_sibling_list = parent.get_child()
            for sibling in potential_sibling_list:
                if sibling not in actual_sibling and sibling.person_name != person_name:
                    actual_sibling.append(sibling)

        return actual_sibling

    def relate_people(self, parent, child):
        """
        :param parent: parent name
        :param child: child name
        :return: None
        """
        #relates the parent and child

        parent_object = self.family_tree[parent]
        child_object = self.family_tree[child]
        if child_object.add_parent(parent_object) == True:
            parent_object.add_child(child_object)




    def save(self, file_name):
        """
        :param file_name: file input that the user wants to save
        :return:
        """
        #iterates through the family tree and then calls in the jsonify function from person class for formatting.

        object_dumping = {}
        for i in self.family_tree:
            print(self.family_tree[i].jsonify())
            object_dumping.update(self.family_tree[i].jsonify())
        with open(file_name, 'w') as write_file:
            write_file.write(json.dumps(object_dumping))


    def load(self, file_name):
        """
        :param file_name: file that is being loaded
        :return: dictionary
        """


        with open(file_name, 'r') as read_json:
            the_entire_file = read_json.read()
            the_entire_dictionary = json.loads(the_entire_file)

            #creates person object
            for person in the_entire_dictionary.keys():
                self.add_person(person)

            #iterates through the whole dictionary
            for person in the_entire_dictionary.keys():
                #creates parent relationship
                for parent_name in the_entire_dictionary[person]['Parent']:
                    self.family_tree[person].add_parent(self.family_tree[parent_name])
                # creates child relationship
                for child_name in the_entire_dictionary[person]['Child']:
                    self.family_tree[person].add_child(self.family_tree[child_name])








if __name__ == '__main__':
    family_Dynasty = DynasticDescent()

    is_done = False
    while not is_done:
        next_step = input("What would you like to do next? ")

        if next_step == 'add':
            person_name = input('What is the name of the human? ')
            family_Dynasty.add_person(person_name)

        elif next_step == 'relate':
            person_one = input('What is the name of the person human? ')
            person_two = input('What is the name of the child human? ')
            family_Dynasty.relate_people(person_one, person_two)

        elif next_step == 'get parents':
            starting_parent = input('What is the name of the parent do you want? ')
            starting_parent_object = family_Dynasty.family_tree[starting_parent] #creates the object
            print_parent = family_Dynasty.find_parents(starting_parent_object, 1)

            for parent in print_parent:
                print('The parents are: ', parent.person_name)

            if len(print_parent) == 0:
                print("There are no grandparents.")

        elif next_step == 'get grandparents':
            starting_person = input("what is the name of the starting human? ")
            starting_person_object = family_Dynasty.family_tree[starting_person] #creates object

            print_grandparent = family_Dynasty.find_parents(starting_person_object, 2)

            for grandparent in print_grandparent:
                print('The grandparents are: ', grandparent.person_name)

            if len(print_grandparent) == 0:
                print("There are no grandparents.")


        elif next_step == 'get descendants':
            starting_human = input('What is the name of the starting human? ')
            degree_descends = int(input('What is the degree of descent? '))
            starting_person_object = family_Dynasty.family_tree[starting_human]
            print_descendants = family_Dynasty.find_children(starting_person_object, degree_descends)
            #iterates through the print_descendants to print the names
            for descedants in print_descendants:
                print('The descendants are: ', descedants.person_name)
            if len(print_descendants) == 0:
                print("There are no descedants.")

        elif next_step == 'get ancestors':
            starting_ancestors = input('What is the name of the starting human? ')
            degree_ancestor = int(input('What is the degree of ancestors? '))
            starting_person_object = family_Dynasty.family_tree[starting_ancestors]
            print_ancestors = family_Dynasty.find_parents(starting_person_object, degree_ancestor)

            for ancestor in print_ancestors:
                print('The ancestors are: ', ancestor.person_name)
            if len(print_ancestors) == 0:
                print("There are no ancestors.")

        elif next_step == 'get siblings':
            starting_sibling = input('What is the starting sibling name? ')
            sibling_list = family_Dynasty.get_siblings(starting_sibling)
            for sibling in sibling_list:
                print('The siblings are:', sibling)
            if len(sibling_list) == 0:
                print('There are no siblings.')

        elif next_step == 'load tree':
            load_input = input('What is the file name to load? ')
            family_Dynasty.load(load_input)
            print('Tree loaded.')

        elif next_step == 'save tree':
            save_input = input('What is the file name to save? ')
            family_Dynasty.save(save_input)
            print('Tree saved.')

        elif next_step == 'quit':
            is_done = True

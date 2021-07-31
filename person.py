
class Person:

    def __init__(self, person_name):
        """
        :param person_name:
        """
        self.parent_list = []
        self.child_list = []
        self.person_name = person_name


    def get_child(self):
        """
        :return: list of child object
        """
        return self.child_list


    def get_parent(self):
        """
        :return: list of parents object
        """
        return self.parent_list


    def add_child(self, child):
        """
        :param child: string of child name
        :return: None
        """
        self.child_list.append(child)



    def add_parent(self, parent):
        """
        :param parent: string of parent name
        :return: None
        """
        #boolean to make sure no more than 2 parents
        if len(self.parent_list) > 2:
            return False
        else:
            self.parent_list.append(parent)
            return True

    def jsonify(self):
        """
        :return:
        """
        #iterates through the parent list to create parent name
        save_parent_list = []
        save_child_list = []
        for parent in self.parent_list:
            save_parent_list.append(parent.person_name)

        for child in self.child_list:
            save_child_list.append(child.person_name)

        return {self.person_name: {'Parent': save_parent_list, 'Child': save_child_list}}

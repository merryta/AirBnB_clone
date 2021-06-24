#!/usr/bin/python3
"""
console module
"""
import cmd
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """class HBNBCommand"""
    prompt = "(hbnb)"

    __classes = {
        "BaseModel"
        }
    def emptyline(self):
        """does nothing when an empty line is invoked"""
        pass

    def do_quit(self, arg):
        """quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF invocation to quit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        creates a new instance of BaseModel, saves it into JSON
        File and prints the id
        """
        if len(arg) ==  0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id>
        Prints a string representation of an instance based on class
        name and id"""
        obj_dict = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg[0], arg[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class_name> <id>
        Deletes an instance based on the class name and id
        and save the changes to a json file"""
        obj_dict = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj_dict:
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg[0], arg[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all <class>, class is optional
        Prints all string representation of all instances
        based or not on the class name.
        """
        if len(arg) > 0 and arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg) > 0 and arg[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_update(self, arg):
        """Usage: update <class name> <id> <attribute name>
        "<attribute value>"
        Updates an instance based on the class name and id
        by adding or updating attribute
        """
        if len(arg) == 0:
            print("** class name missing **")
        for obj in storage.all().values():
            if len(arg) > 0 and arg[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                

if __name__ == '__main__':
    HBNBCommand().cmdloop()

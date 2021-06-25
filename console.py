#!/usr/bin/python3
"""
console module
"""
from shlex import split
import cmd
from models.base_model import BaseModel
from models import storage

class HBNBCommand(cmd.Cmd):
    """class HBNBCommand"""
    prompt = "(hbnb)"

    __classes = {
        "BaseModel",
        "User",
        "State"
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
        args = parse(arg)
        if len(args) ==  0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(args[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id>
        Prints a string representation of an instance based on class
        name and id"""
        args = parse(arg)
        obj_dict = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(args[0], args[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class_name> <id>
        Deletes an instance based on the class name and id
        and save the changes to a json file"""
        obj_dict = storage.all()
        args = parse(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in obj_dict:
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(args[0], args[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all <class>, class is optional
        Prints all string representation of all instances
        based or not on the class name.
        """
        args = parse(arg)
        if len(args) > 0 and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(args) > 0 and args[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(args) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_update(self, arg):
        """Usage: update <class name> <id> <attribute name>
        "<attribute value>"
        Updates an instance based on the class name and id
        by adding or updating attribute
        """
        args = parse(arg)
        obj_dict = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        if len(args) == 1:
            print("** instance id missing **")
        if "{}.{}".format(args[0], args[1]) not in obj_dict.keys():
            print("** no instance found **")
        if len(args) == 2:
            print("** attribute name missing **")
        if len(args) == 3:
            print("** value missing **")
        if len(args) == 4:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                cast = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = cast(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        storage.save

def parse(arg):
    """converts a string to a list of arguements"""
    args = split(arg)
    return args
if __name__ == '__main__':
    HBNBCommand().cmdloop()

#!/usr/bin/python3
"""
console module
"""
import re
from shlex import split
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """class HBNBCommand"""
    prompt = "(hbnb)"

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def default(self, line):
        """invoked when an invalid arguement is encountered"""
        flag = match = re.search(r"\.", line)
        if flag is not None:
            arg = line.replace("(", ".(")
            args = arg.split(".")
            if args[0] in HBNBCommand.__classes and args[2] is not None:
                if args[1] == "all":
                    return self.do_all(args[0])
                elif args[1] == "count":
                    return self.do_count(args[0])
                elif args[1] == "show":
                    new = args[2].replace("(", "")
                    new = new.replace(")", "")
                    return self.do_show("{} {}".format(args[0], new))
                elif args[1] == "destroy":
                    new = args[2].replace("(", "")
                    new = new.replace(")", "")
                    return self.do_destroy("{} {}".format(args[0], new))
                elif args[1] == "update":
                    new = args[2].replace("(", "")
                    new = new.replace(")", "")
                    braces = re.search(r"\{(.*?)\}", new)
                    if braces is not None:
                        new = new.replace(", {", ".{")
                        print(new)
                        new = new.split(".")
                        print(new)
                        print(new[0])
                        print(new[1])
                        return self.do_update(args[0] + '~' +
                                              new[0] + '~' + new[1])
                    else:
                        new = new.split(",")
                        _id = new[0]
                        name = new[1]
                        value = new[2]
                        return self.do_update(args[0] + ' ' + _id +
                                              ' ' + name + ' ' + value)
                else:
                    print("*** Unknown syntax: {}".format(line))
            else:
                print("*** Unknown syntax: {}".format(line))
        else:
            print("*** Unknown syntax: {}".format(line))

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
        if len(args) == 0:
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
        braces = re.search(r"\{(.*?)\}", arg)
        if braces is not None:
            args = arg.split('~')
            args[1] = args[1].replace("'", "")
        else:
            args = parse(arg)
        print(args)
        obj_dict = storage.all()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            # evaluating a dictionary presence, otherwise value missing
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(args) == 4:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                cast = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = cast(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            for key, value in eval(args[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in
                        {str, int, float}):
                    cast = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = cast(value)
                else:
                    obj.__dict__[key] = value
        storage.save

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        retrieves the count of instances of a given class
        """
        args = parse(arg)
        count = 0
        for obj in storage.all().values():
            if args[0] == obj.__class__.__name__:
                count += 1
        print(count)


def parse(arg):
    """converts a string to a list of arguements"""
    args = split(arg)
    return args
if __name__ == '__main__':
    HBNBCommand().cmdloop()

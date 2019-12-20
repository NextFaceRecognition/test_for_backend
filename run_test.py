import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '--method',
    type=str,
    default='check_person',
    help='''method is the option indicates run test script to do 
        what action. There are two options: 
            1) add_face
            2) check_person.
    '''
)

parser.add_argument(
    '--image_dir', 
    type=str,
    default='data/',
    help='''image_dir is the folder storing images to be uploaded.'''
)

parser.add_argument(
    '--verify_mode',
    type=str,
    default='1v1',
    help='''Mode of verification, '1v1' or '1vn'.'''
)

# run test script begin.
import sys

from test.print_helper import PrintFunctions
from test.test_method import test_add_face_method, test_check_person_method


def run_test():
    args = parser.parse_args()
    PrintFunctions.print_arguements(args)
    if args.method == 'add_face':
        test_add_face_method(args.image_dir)
    elif args.method == 'check_person':
        test_check_person_method(args.image_dir, 
                                 args.verify_mode)
    else:
        PrintFunctions.print_error('Error: method {} not allowed!'
                                   .format(args.method))
        sys.exit(1)
        

if __name__ == '__main__':
    run_test()
    
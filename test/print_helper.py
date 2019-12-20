

class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

class PrintFunctions(object):
    
    def _print_msg(msg, type_=bcolors.ENDC, end='\n'):
        print('{}{}{}'.format(type_, msg, bcolors.ENDC), end=end)
        
    def print_error(msg, end='\n'):
        PrintFunctions._print_msg(msg, 
                                  type_=bcolors.FAIL,
                                  end=end)

    def print_warning(msg, end='\n'):
        PrintFunctions._print_msg(msg, 
                                  type_=bcolors.WARNING,
                                  end=end)
        
    def print_success(msg, end='\n'):
        PrintFunctions._print_msg(msg, 
                                  type_=bcolors.OKGREEN,
                                  end=end)
    
    def print_ok_blue(msg, end='\n'):
        PrintFunctions._print_msg(msg, 
                                  type_=bcolors.OKBLUE,
                                  end=end)
    
        
    def print_arguements(args='\n'):
        if not isinstance(args, dict):
            args = args.__dict__
        print('{}{}{}'.format('='*10, ' Arguments ', '='*10))
        for key, value in args.items():
            print('{}: {}'.format(key, value))
        print('=' * 31)


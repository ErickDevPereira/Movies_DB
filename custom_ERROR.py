class NotAnOption(Exception):

    def __init__(self, given_arg, /, *args):
        self.msg = f'ERROR >> {given_arg} is not an allowed argument.\nList of allowed arguments: \n {[argument for argument in args]}'
        super().__init__(self.msg)
    
    def __str__(self):
        return f"{self.msg}\n\nABOUT THE ERROR >> This error raises when you use an wrong option for a function!"
    
if __name__ == '__main__':
    raise NotAnOption('x', 'separate', 'together')
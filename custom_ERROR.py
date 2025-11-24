class NotAnOption(Exception):

    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)
    
    def __str__(self):
        return f"{self.msg}\nABOUT THE ERROR >> This error raises when you use an wrong option for a function!"
    
if __name__ == '__main__':
    raise NotAnOption('Ainain')
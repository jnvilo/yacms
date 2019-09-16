from  faker import Faker
import random


def get_fake_contents(num_paragraphs):
    fake = Faker()
    
    paragraphs = []
    for c in range(num_paragraphs):
        num_sentences = random.randint(5,10)
        paragraphs.append(" ".join(fake.paragraphs(num_sentences)))
        
    return "\n\n".join(paragraphs)


escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}

def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string



registry = {}

def p_decorate(func):
    print(func.__name__)
    registry.update({func.__name__:func})
    return func

class Wrapped(object):
    
    @p_decorate
    def myfunc(self):
        print("wrapped")
        
    @p_decorate
    def myfunc2(self):
        pritn("myfunc2")
        
w = Wrapped()
w.myfunc()

print(registry)
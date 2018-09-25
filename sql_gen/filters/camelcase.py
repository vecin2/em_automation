def camelcase(value):
    return "juan"

def convert_to_camelcase(input_string):
    words = input_string.split(' ') #Splitting the string into words
    capitalized = [] #initializing a list to store each word after making first letter capital 
    for word in words:
        final_words = word[0].upper() + word[1:] #Converting first letter to upper case and appending it with remaining letters
        capitalized.append(final_words) #Appending all words into capitalized list
    output = ' '.join(capitalized) #At last joining each word togather to make a string
    return output

def get_template_filter():
    return camelcase

class CamelcaseFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, display_text):
        return "pedro"

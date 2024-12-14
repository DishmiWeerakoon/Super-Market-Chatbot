import re
import random
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

#download resources for tokenization and lemmatization
nltk.download('punkt')
nltk.download('wordnet')

def delete_file_contents(file_path):
  with open(file_path, 'w') as file:
    pass

def get_item_details(words, type):
  item_shelfnumber ={}
  with open("itemLists.txt", "r") as file: #open the text file which contains the item list and shelf numbers
    for line in file:
        item_name, shelf_number = line.strip().split(',') # Split the line by comma
        for word in words:
          if word.lower() == item_name.lower(): # Check if the word is in the line
            if type == "shelf_number":
              item_shelfnumber[item_name] = shelf_number
  return item_shelfnumber

def preprocess_text(text):
    #tokenize the reply
    tokens = word_tokenize(text)

    #convert plural words to singular (lemmatization)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

class KMartChatBot:
  #dictionary containing intents and regex for each intent
  wordDictionary = {
    "search_shelfnumber": r"shel(f|ves)\b",  #shelf or shelves
}
  
  #possible negative responses
  negative_responses = ("no", "nope", "nah", "nothing more", "nothing", "nothing else", "that's all", "not a chance", "sorry")
  #possible keywords which exits the conversation
  exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
  #random starting questions
  random_questions = (
        "How can I help you? I can give you the shelf numbers of the goods\n",
        "How can I assist you? I can give you the shelf numbers of the goods\n",
        "What are you looking for? I can give you the shelf numbers of the goods\n",
        "what are things you need to buy? I can give you the shelf numbers of the goods\n"
    )
 
  #remove punctuation from string
  def remove_punctuation(self, text):
    return text.translate(str.maketrans("", "", string.punctuation))
  
  def greet(self):
    file_path = 'shelf_numbers.txt'
    delete_file_contents(file_path)
    self.name = input("Hello Customer! Welcome to KMart. What's your name? \n")
    willShop = input(f"Hello, {self.name}! Are you looking to do some shopping? \n")

    if willShop in self.negative_responses:
      print("Have a nice day!")
      return
    self.shopping()

  def negative_exit(self, reply):
    if reply in self.negative_responses:
      print("Have a nice day!")
      return True
    
  def make_exit(self, reply):
    if reply in self.exit_commands:
      print(f"Thank you for choosing KMart, {self.name}! Have a nice day!")
      return True
    
  def shopping(self):
    reply = self.remove_punctuation(input(random.choice(self.random_questions)).lower())
    while not self.make_exit(reply) and not self.negative_exit(reply):
      reply = input(self.match_reply(reply))
  
  def match_reply(self, reply):
    for key, value in KMartChatBot.wordDictionary.items():
        intent = key
        regex = value
        found = re.search(regex, reply)
        if found:
            if intent == "search_shelfnumber":
                return self.search_shelf_number(reply)
    return self.no_match() #If no matches were found in the loop, then return no match intent

  def search_shelf_number(self, reply):
    response = (
      "What else do you want to know?\n",)

    lemmatized_tokens = preprocess_text(reply)
    #shelf number searching
    item_shelfnumber = get_item_details(lemmatized_tokens, "shelf_number")

    response1 =""
    if(len(item_shelfnumber) == 0):
      return "Sorry, I couldn't locate the item. Please ask from a staff member. Anything else?\n"
    for item, shelf_number in item_shelfnumber.items():
      response1 += f"-{item} - shelf number {shelf_number}\n"
    with open('shelf_numbers.txt', 'a') as file:
      file.write(response1)
    return response1 + random.choice(response)

  def no_match(self):
    response =(
      "I am not sure what you are looking for. Can you be more precise?\n",
      "Could you provide more details? I am not sure what you are looking for.\n"
    )
    return random.choice(response)   

myBot = KMartChatBot()
myBot.greet()     
    
  

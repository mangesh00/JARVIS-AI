# Import required libraries 
from AppOpener import close, open as appopen # Import function to open and close apps.
from webbrowser import open as webopen # Import web browser functionlity.
from pywhatkit import search, playonyt # Import functions for Google search and Youtube playback.
from dotenv import dotenv_values # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup # Import BeautifulSoup for parsing HTML content.
from rich import print # Import rich for styled console output.
from groq import Groq # Import Groq for AI chat functionalities.
import webbrowser # Import webbrowser for opening URLs.
import subprocess # Import subprocess for interacting with the system.
import requests # Import requests for making HTTP requests.
import keyboard # Import Keyboard for keyboard-releted action.
import asyncio # Import asyncio for asynchronous porgramming.
import os # Import os for operating system functionalities.

# Load environment variables from .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey") # Retrieve the Groq API Key.

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API Key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may nedd-don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System messages to provided context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc. "}]

# Function to perform a Google serach.
def GoogleSearch(Topic):
    search(Topic) # Use pywhatkit's search function to perform a Google search.
    return True  # Indicate sucess.

# Function to generate content using AI and save it to a file.
def Content(Topic):
    
    # Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe' # Default text editor
        subprocess.Popen([default_text_editor, File]) # Open the file in notepad.
    
    # Nested functions to generate content using the AI chatbot.
    def ContentWriteAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) # Add the user's prompt to messages.
        
        comletion = client.chat.completions.create(
            model="mixtral-8x7b-32768", # Specify the AI model.
            messages=SystemChatBot + messages, # Include system instructions and chat history.
            max_tokens=2048, # Limit the maximum token in the response.
            temperature=0.7, # Adjust response randomness.
            top_p=1, # Use nucleus sapmling for response diversity.
            stream=True,
            stop=None # Allow the model to determine stopping condition.            
        )
        
        Answer = "" # Initialize an empty string for the response.
        
        # Process streamed response chunks.
        for chunk in comletion:
            if chunk.choices[0].delta.content: # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content # Append the content to the answer.
                
        Answer = Answer.replace("</s>", "") # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer}) # Add the AI's response to messages.
        return Answer
    
    Topic: str = Topic.replace("Content ", "") # Remove "Content " from the topic.
    ContentByAI = ContentWriteAI(Topic) # Generate content to the file.
    
    # Save the generated content to text file.
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) # Write the content to the file.
        file.close()
        
    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt") # Open the file in Notepad.
    return True # Indicate success.

# Function to serach for a topic on Youtube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" # Construct the Youtube search URL.
    webbrowser.open(Url4Search) # Open the search URL in a web browser..
    return True # Indicate Success.

# Function to play a video on Youtube.
def PlayYouTube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True # Indicate success.

# Function to open an application or relevent webpage.
def OpenApp(app, sess=requests.session()):
    
    try:
        appopen(app, match_closest=True, output=True, throw_error=True) # Attempt to open the app.
        return True # Indicate success.
    except:
        # Nested function to extract links from HTML content.
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser') # Parse the HTML Content.
            links = soup.find_all('a', {'jsname': "UWckNb"}) # Find relevant links.
            return [links.get('href') for link in links] # Return the links.
        
        # Nested function to perform a google serach and retrieve HTML.
        def search_google(query):
            url = f"https://www.google.com/search?q={query}" # Construct the Google search URL.
            headers = {"User-Agent": useragent} # Use the predefined user-agent.
            response = sess.get(url, headers=headers) # Perform the GET request.
            
            if response.status_code == 200:
                return response.text # Return to the HTML content.
            else:
                print("Failed to retrive search results.") # Print an error message.
                return None
        
        html = search_google(app) # Perform the Google search.
        
        if html:
            link = extract_links(html)[0] # Extract the first link from the search results.
            webopen(link) # Open the link in web browser.
            
        return True # Indicate success.
    
# Function to close an application.
def CloseApp(app):
    
    if "Chrome" in app:
        pass # Skip if the app id Chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True) # Attempt to close the app.
            return True # Indicate success.
        except:
            return False # Indicate failure.
        
# Function to execute system-level commands.
def System(command):
    
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute") # Simulate the mute key press.
    
    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume unmute") # Simulate the unmute key press.
    
    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up") # Simulate the Valume up key press.
        
    # Nested function to increase the system volume.
    def volume_down():
        keyboard.press_and_release("volume down") # Simulate the Valume down key press.
        
    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
        
    return True # Indicate success.

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    
    funcs = [] # List to store asynchronous tasks.
    
    for command in commands:
        if command.startswith("open "): # Handle "Open" commands.
            
            if "open it" in command: # Ignore "open it" commands.
                pass
            
            if "open file" in command: # Ignore "open file" commands.
                pass
            
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule app opening.
                funcs.append(fun)
        
        elif command.startswith("general "): # Placeholder for general commands.
            pass
        
        elif command.startswith("realtime "): # Placeholder for real-time commands.
            pass
        
        elif command.startswith("close "): # Handle for close commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # Schedule app closing.
            funcs.append(fun)
                
        elif command.startswith("play "): # Handle for Play commands.
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play ")) # Schedule  Youtube playback.
            funcs.append(fun)

        elif command.startswith("content "): # Handle for content commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content ")) # Schedule content creation.
            funcs.append(fun)

        elif command.startswith("google search "): # Handle for google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")) # Schedule Google Search.
            funcs.append(fun)
        
        elif command.startswith("system "): # Handle for System commands.
            fun = asyncio.to_thread(System, command.removeprefix("system ")) # Schedule System commands. 
            funcs.append(fun)
        
        else:
            print(f"No Function Found. For {command}") # Print an error for unrecognized commands.
            
    results = await asyncio.gather(*funcs) # Execute all tasks concurrently.
    
    for result in results: # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result
            
# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands): # Translate and execute commands.
        pass
    return True # Indicate success.

# if __name__=="__main__":
#     asyncio.run(Automation(["open facebook", "open instagram", "open telegram", "open github", "play milleniour", "content song for me"]))
        
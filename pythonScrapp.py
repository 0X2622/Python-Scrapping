from bs4 import BeautifulSoup
import requests
import time

#Simple python script used to generate headers and send the data to a specific server, and then analyzes the response header and data from the
#server.


def sendOptionsRequest(url):
    response = requests.options(url) # options is the parameter that allows user to get a respone of available methods.
    if response.status_code == 200:
        allowed_methods = response.headers.get('Allow', '')
        return allowed_methods.split(', ')
    else:
        return []

#constructs payloads and headers and then send the data to the server, and also asks data from the server.
#The parameters are userinformation that is sent into the server registration form.
def sendRecieveRequest(username, password, password2, carplate):

    session = requests.Session() 
    
    #payload with userinformation that is sent to the header
    payload = {
            "username": username, 
            "plate": carplate, 
            "password": password,
            "password2": password2}
    
    # Calculate the size of the payload
    #this line of code calculates the length of the URL-encoded payload that will be sent in the request. 
    # This length is then used to set the Content-Length header in the HTTP request.
    contentLength = len('&'.join([f'{key}={value}' for key, value in payload.items()]))
 
    #creating request header for the server.
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(contentLength),
        'Host': 'localhost:3000',
        'Origin': 'http://localhost:3000',
        'Referer': 'http://localhost:3000/register',        
        'User-Agent': 'python-requests/2.31.0'
    }
    
    print("headers:")
    print(headers) #test print
    start_time = time.time()   # Start a timer to be able to time the response header from the server.
    
    responeData = session.post("http://localhost:3000/signup", data=payload, headers=headers) #inserts user data to the signup form
    getData = session.get("http://localhost:3000/register") #get data from the registration webpage

    # Calculate round trip time (response time) from the server
    end_time = time.time()
    responseTime = (end_time - start_time) * 1000 #converting to milliseconds
    
    #htmlData = soup.find_all('div', class_='form-group')
    #print(htmlData)

    return responeData, responseTime, getData #returning useful information from the server.



#prints the data from the server page and also headers.
def printData(responseData, responseTime, getData):
 
    
    data = getData.text #data will be the HTML content in text format.
    soupedData = BeautifulSoup(data, 'lxml')

    print("HTML CONTENT: ")
    print(soupedData.prettify()) #pritns the complete HTML data from the server in a more readable format.   

    # Print the request header
    print("Request Header:")
    print(responseData.request.headers)

    # Print the response header
    print("\nResponse Header:")
    print(responseData.headers)

    # OBS: this checks if the signup rescource "/signup" was successfully found, but it doesn't say whether the actual user registration was 
    # successfull or not. -> need to fix.
    if responseData.status_code == 200:
        print("\nRegistration/Signup was successful!")
    else:
        print("\nRegistration/Signup failed. Status code:", responseData.status_code)


    # Format the response time to display a maximum of three decimal places -> analysera hur denna funkar
    formattedResponseTime = "{:.3f}".format(responseTime)

    # Print the response time in milliseconds
    print("\nResponse time (milliseconds):", formattedResponseTime, "ms")

    return 


#initiating user values 
print("")
username = input("Enter username: ")
carplate = input("Enter carplate: ")
password = input("Enter password: ")
password2 = input("repeat password ")
print("") #blank space


# Check allowed methods for the /signup endpoint
allowed_methods_signup = sendOptionsRequest("http://localhost:3000/signup")
print("Allowed methods for /signup:", allowed_methods_signup)

# Check allowed methods for the /register endpoint
allowed_methods_register = sendOptionsRequest("http://localhost:3000/register")
print("Allowed methods for /register:", allowed_methods_register)

responseData, responseTime, getData = sendRecieveRequest(username, password, password2, carplate) #creates and fetches data 
printData(responseData, responseTime, getData) #prints data

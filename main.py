from linkedin_api import Linkedin
import sys
import getpass
from optparse import OptionParser


email = None
password = None



def get_options():
    parser = OptionParser()
    parser.add_option("-k", "--keyword", dest="keyword",
                    help="Write company keyword to search")

    parser.add_option("-e", "--email",
                    dest="emailformat",
                    help="Write emailformat to concatenate example 'hotmail.com' ")

    parser.add_option("-s", "--seperator",
                dest="seperator",
                help="Enter seperator between firstname and last name")

    (options, args) = parser.parse_args()
    if not options.emailformat:
        parser.error("Please enter the email format! example : -e hotmail.com, gmail.com etc.")
    if not options.keyword:
        parser.error("Please enter company keyword to search! example : -k facebook, google")
    if not options.seperator:
        parser.error("Enter seperator between firstname and last name examples: -s '.' ")
    return options

def main():
    global email
    global password
    print(email)
    print(password)
    options = get_options()
    keyword = options.keyword
    emailformat = options.emailformat
    seperator = options.seperator
    print("[+] emailformat : ",emailformat)
    print("[+] seperator : ",seperator)
    print("[+] keyword : ",keyword)
    print("[+] output example : firstname"+seperator+"lastname@"+emailformat)

    # Authenticate using any Linkedin account credentials
    api = Linkedin(email, password)
    people = api.search_people(keyword_company=keyword)
    print(people)
    exit()
    results = []

    for person in people:
        #print(person['public_id'])
        try:
            user = api.get_profile(person['public_id'])
        except Exception as e:
            print(e)
        try:
            email = user['firstName'] + "." + user['lastName'] + "@" + emailformat +"\n"
            results.append(email.lower())
            print(user['firstName'] + "." + user['lastName'])
        except Exception as e:
            print(e)

    with open("mails_output.txt","w+") as output:
        for i in results:
            output.write(i)
            output.write("\n")

def read_config():
    with open("credentials.txt","r+") as configfile:
        global password
        global email
        context = configfile.readlines()
        email, password = context[0], context[1]
        email = (email.split(":")[1]).rstrip("\n")
        password = (password.split(":")[1]).rstrip("\n")
        if email == "" or password == None:
            print("[-] Please give credentials from config file")
            exit()

read_config()
main()

#some notes
#urn:li:country:tr

# GET a profiles contact info
#contact_info = api.get_profile_contact_info('billy-g')

# GET 1st degree connections of a given profile
#connections = api.get_profile_connections('1234asc12304')

# GET a profile
# profile = api.get_profile('ahmtcnn')
# print(profile)
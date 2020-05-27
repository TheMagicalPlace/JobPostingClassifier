import click
import base64

from ui.file_tree_setup import *
from scrapers import IndeedClient,LinkdinClient

class EncryptionHandler:


    @classmethod
    def encrypt(cls,username,password):
        with open(os.path.join(os.getcwd(), "user_preferences", "settings.json"),"r+") as settings_file:
            settings = json.loads(settings_file.read())
            settings["Linkedin_Info"]["Username"] = base64.encode(username)
            settings["Linkedin_Info"]["Password"] = base64.encode(password)
            settings_file.write(json.dumps(settings))

    @classmethod
    def decrypt(cls):
        with open(os.path.join(os.getcwd(), "user_preferences", "settings.json"), "r") as settings_file:
            settings = json.loads(settings_file.read())
            euse = settings["Linkedin_Info"]["Username"]
            epass = settings["Linkedin_Info"]["Password"]
        return base64.decode(euse),base64.decode(epass)



def first_time_setup():
    """ Setting up user settings file on first time use"""
    try:
        os.mkdir(os.path.join(os.getcwd(), 'user_preferences'))
        user_preferences = {
            "Linkedin_Info":
            {
                "Username" : "Null",
                "Password" : "Null"
            },
            "IndeedInfo" : "Not Implimented",
            "TermEquivalencies":
            {
                "dummy_search_term" : ["dummy equivalency 1","dummy equivalency two"]
            }

        }
        with open(os.path.join(os.getcwd(),"user_preferences","settings.json"),"w") as settings:
            settings.write(json.dumps(user_preferences))
    except FileExistsError:
        pass


@click.group()
def opening(**options):
    """
    Welcome to my scikit-learn based Smart Job Classifier!
    
    Currently this program consists of two seperate parts, the first, which can be accessed by using the
    search option will allow you to search and save job postings off of either Indeed of linkden
    based on a given search term. The second option "classify" sorts any unclassified jobs into either "good" or "bad" based
    on user-supplied job data. Alternatively, using the all command will allow you to search and classify
    jobs in the same command.
    
    Note that if this is your first time using this program, or if you are using an entierly new search term, 
    you must first use the --search option and manually sort some initial job descriptions in order to give the
    model a basis for sorting. Detailed instructions are given within the search option for how to do this.
    """



@opening.command()

@click.argument("job_board", default="None")
@click.argument("search_term", default="None")
@click.argument("location",default="United States")
@click.argument("equivlant_to", default="None")
@click.argument("no_results", default=100)
@click.option("--no-term-checking", is_flag=True, help="""Created a new file tree for the search term. Use 'search --help' for more information""")
@click.option("--help", is_flag=True)
def search(job_board, search_term,location, equivlant_to, no_results, **options):
    first_time_setup()

    scrapers = {"Indeed":IndeedClient,"Linkedin":LinkdinClient}

    """Searches and saves job postings based on a user selected term"""
    if options["help"]:
        click.echo\
    (
    """

    USAGE interface.py --search [JOB_BOARD] [SEARCH_TERM] [EQUIVALENT_SEARCH_TERM] [NUMBER OF RESULTS]

    ARGUMENTS : 

        JOB_BOARD:
            Accepts either "Indeed" or "LinkedIn" (not case sensitive)
        
        LOCATION:
            The location to search for job postings
        
        SEARCH_TERM:
            The term to search the selected job boards (not case sensitive)

        EQUIVALENT_SEARCH_TERM:
            default = "None"

            Used to specify if the results from the supplied search term should be included under the umbrella
            of another search term for sorting and model training. For example, if
            'Computer Programmer' was previously searched, searching "Entry Level Computer Programmer" and setting
            [EQUIVALENT_SEARCH_TERM] to 'Computer Programmer' would put the results from "Entry Level Computer Programmer"
            in the same file tree as 'Computer Programmer'. (not case sensitive)

            If not supplied, a new file tree is created for the search term if one does not already exist.

        NUMBER_OF_RESULTS:
            default = 50
            
            Number of NEW job postings to find, postings that have already been found and downloaded don't count
            when determining when to stop.

    OPTIONS:

        --no-term-checking:
            By default, the program will try and file results under an equivalent search term if one had been
            specified for the search term before i.e. if "Entry Level Computer Programmer" had been searched as equivalent 
            to "Computer Programmer" before, the search will default to putting the results under it's file tree. 
            To overwrite this behavior, use this option. Note that this will be applied to all future searches for this
            term unless a new equivalent search term is assigned.
    """
    )
        return
    if options["no_term_checking"] or equivlant_to == "None":
        equivlant_to = search_term;

    # Normalizing terms
    job_board = job_board.lower().title()
    search_term = search_term.lower().title()
    equivlant_to = equivlant_to.lower().title()

    # Checking validity of supplied terms and file paths

    if job_board=="None" or search_term=="None":
        click.echo("A job board and search term must be supplied")
        return
    elif job_board not in ["Indeed","Linkedin"]:
        click.echo("Invalid job board given, currently job posting searching is only available for LinkedIn or Indeed")
        return
    elif not os.path.isdir(os.path.join(os.getcwd(),search_term)):
        # creating a new folder for a new search term
        file_setup(search_term)
    elif not os.path.isdir(os.path.join(os.getcwd(),equivlant_to)) and equivlant_to != "None":
        click.echo("File tree for equivlant search term not found, are you sure you spelled it right?")
        return


    # TODO feed user and password directly to init + dont save
    # create scraper object and call
    u, p = get_linkedin_info()
    scraper = scrapers[job_board](search_term,equivlant_to,location)

    if job_board == "Linkedin":
        u,p = get_linkedin_info()
        scraper(no_results,*get_linkedin_info())


def get_linkedin_info():

    # try to find existing settings
    with open(os.path.join(os.getcwd(), "user_preferences", "settings.json"), "r") as settings_file:

        tmp = json.loads(settings_file.read())
        print(tmp)
        if tmp["Linkedin_Info"]["Username"] != "Null":
            return EncryptionHandler.decrypt()

    # otherwise get them from thew user
    user = input("Please input LindedIn username")
    passw = str(input("Please input LinkedIn password"))
    save = str(input("Would you like to save your login information for future use (Y/n) ?"))
    if save == "Y":
        EncryptionHandler.encrypt(user,passw)
    else:
        return user,passw






if __name__ == '__main__':
    opening()
    search()
import sys, os

import click

@click.group()
def opening(**options):
    """
    Welcome to my scikit-learn based Smart Job Classifier!
    
    Currently this program consists of two seperate parts, the first, which can be accessed by using the
    search option will allow you to search and save job postings off of either indeed of linkden
    based on a given search term. The second option "classify" sorts any unclassified jobs into either "good" or "bad" based
    on user-supplied job data. Alternatively, using the all command will allow you to search and classify
    jobs in the same command.
    
    Note that if this is your first time using this program, or if you are using an entierly new search term, 
    you must first use the --search option and manually sort some initial job descriptions in order to give the
    model a basis for sorting. Detailed instructions are given within the search option for how to do this.
    """

@opening.command()
@click.argument("job_board")
@click.argument("search_term")
@click.argument("equivlant_to",default="None")
@click.argument("no_results",default=100)
@click.option("--no-term-checking",default=False)
def search(job_board,search_term,equivlant_to,no_results,**options):




    print(job_board,search_term,no_results)
    """"Search selected job board for jobs

    USAGE:

        interface.py --search [JOB_BOARD] [SEARCH_TERM] [EQUIVALENT_SEARCH_TERM] [NUMBER OF RESULTS]
    
    ARGUMENTS : 
    
        JOB_BOARD:
            Accepts either "Indeed" or "LinkedIn" (not case sensitive)
            
        SEARCH_TERM:
            The term to search the selected job boards (not case sensitive)
            
        EQUIVALENT_SEARCH_TERM:
            default = "None"
        
            Used to specify if the results from the supplied search term should be included under the umbrella
            of another search term for sorting and model training. For example, if
            'Computer Programmer' was previously searched, searching "Entry Level Computer Programmer" and setting
            [EQUIVALENT_SEARCH_TERM] to 'Computer Programmer' would put the results from "Entry Level Computer Programmer"
            in the same file tree as 'Computer Programmer'. (not case sensitive)
            
            If not supplied, a new file tree is created for the search term.
        
        NUMBER_OF_RESULTS:
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


    "Asas"
    click.echo("sdasdsad")
    print("yeet")

if __name__ == '__main__':
    opening()

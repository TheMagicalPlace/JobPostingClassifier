import os

def file_setup(search_term):
    """Sets up the file structure used by the program for each search term"""
    try:
        os.mkdir(os.path.join(os.getcwd(),search_term))
    except FileExistsError:
        pass



    # Job Description folders
    for folder in ['Train', 'Results']:
        try:
            os.mkdir(os.path.join(os.getcwd(), search_term, folder))
        except FileExistsError:
            pass
        for subfolder in ['Good Jobs', 'Bad Jobs', 'Neutral Jobs', 'Ideal Jobs']:
            try:
                os.mkdir(os.path.join(os.getcwd(), search_term, folder, subfolder))
            except FileExistsError:
                continue
        if folder == 'Train':
            try:
                os.mkdir(os.path.join(os.getcwd(), search_term, folder, 'Other'))
            except FileExistsError:
                continue
    else:
        # Pre-sort job desc. folder
        try:
            os.mkdir(os.path.join(os.getcwd(), search_term, 'Unsorted'))
        except FileExistsError:
            pass

        # classification models
        try:
            os.mkdir(os.path.join(os.getcwd(),search_term,'Models'))
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join(os.getcwd(), search_term, 'Models','model_files'))
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join(os.getcwd(), search_term, 'Models','old'))
        except FileExistsError:
            pass




if __name__ == '__main__':
    file_setup('Entry Level Computer Programmer')
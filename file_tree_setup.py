import os

def file_setup(search_term):

    try:
        os.mkdir(os.path.join(os.getcwd(),search_term))
    except FileExistsError:
        pass
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
    else:
        try:
            os.mkdir(os.path.join(os.getcwd(), search_term, 'Unsorted'))
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join(os.getcwd(), search_term, 'Discarded'))
        except FileExistsError:
            pass


if __name__ == '__main__':
    file_setup('Chemical Engineer')
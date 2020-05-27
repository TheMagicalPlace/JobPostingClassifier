## Smart Job Classifier

Smart Job Classifier is a tool build to simpilify your job search, especially for entry level canidates applying to large numbers of
jobs. Using this, it is possible to cut down ...TBC

## Installation

Download the latest [release](https://github.com/TheMagicalPlace/JobPostingClassifier/releases) and place it into a folder of your choice. Not that once the main executable is placed into a folder 
it shouldn't be moved out of it, otherwise issues will likely occur.

## Usage

Before getting started, you'll need either/or chromedriver and/or geckodriver. These should be downloaded using the corresponding download buttons on the application, otherwise the application won't know where to find them. I reccomend going with chromedriver, as that has been what this has been mostly tested on, and my limited testing with geckodriver has shown it to be more hit or miss with this application. Once you've downloaded that, you're all set to start using this.


Note that all of the below is also supplied within the application itself. The usage instructions will be broken up for each tab found on the gui of the application.

### Search

Here you can search and download job postings from any of the available job boards. If using LinkedIn a username and password is currently required, and the option to save your credentials for future use is available. Below information is given about what should be input into each field. Note that all terms besides login credentials are not case sensative.

#### FIELDS

Job Board:
Selecting which job board to get data from. Note that with linkedin it is required that you log in. Can optionally save LinkedIn login credentials if desired.

Location:
The location for which to search for job postings.

Search Term:
The term to search the selected job boards.

File Term:
Used to specify which job data folder to save the results of the search to. This defaults to the search term, however in cases where a given field of related jobs can have multiple titles or search terms it is often desirable to include them all as a part of the same dataset for model training and sorting.
For example, if 'Computer Programmer' was previously searched, searching "Entry Level Computer Programmer" and setting the equivalent file term to 'Computer Programmer' would put the results from "Entry Level Computer Programmer" in the same location as those from searching 'Computer Programmer'.

No. of Jobs to Find:
Number of NEW job postings to find, postings that have already been found and downloaded don't count when determining when to stop.

### Train

This section is used to train classification models for use in job sorting. Can be used to create and train models from new data, or to update old models based on newly added data.

#### INSTRUCTIONS

In order to create the models used in this program it is required that some initial information is supplied. This is done by downloading (via the 'Search Tab') and manually sorting job postings according to whether the job posting is an 'Ideal', 'Good', 'Neutral', or 'Bad' job for you. It is reccomended that supply at least 100 jobs for the training data as well as ensuring that the way you are sorting them as accuratly as possible, however the more data you supply for training the more accurate the results will be, as well as reducing the impact of badly sorted jobs on the result. Once this is done you can run the training via 'Train Models', the amount of time taken depends on the number of iterations and amount of training data, however 1-3 hours should be a typical amount of time for the training to complete.

So, in order the steps are:
Download job postings using the 'Search' tab for the file term you are using.
Sort the jobs using the 'Manually Sort Jobs' Button.
Run the training program via 'Train Models'.

#### FIELDS

File Term:
This should be the same term as the search term used previously if this is for completely new models, otherwise use the file term for which you want to update models for.

Iterations Per Round:
The number of times to train the models on the data, higher numbers will increase model accuracy, but take longer. Between 50-150 is reccomended, with minimal improvment for any higher amount. 

### Classify

Used to classify job postings that have already been downloaded but not yet classified. Note that before using this feature you must have previously trained models for the search/file term you are trying to classify. Further information on this is given unter the 'Train' tab as well as in the readme. Note that the classification term is not case sensative.

#### FIELDS

Classification/File Term:
Used to tell the classifier which  search/file term the classification model should be loaded from, as well as where to save the results to.

Clasifier to Use:
(To be implimented)
It is highly reccomended that you leave this set to auto, however if you know what you're doing a model can be manually selected to run instead of the found best one.  

### Train + Classify

Please refer to the the Search and Classify tab info for information on each input field. Only real thing to note is that there
must be an extant file term <b>WITH TRAINED MODELS</b> selected for combined use.

## Contributing

Note that the code in the main branch isn't always reflective of the current release, I'll try to keep the release code under the 'release' branch, but they may not always be up to date.

For the most part, what any given section of the code is doing should have some sort of documentation. Notable exceptions
to this include the GUI code, which is only minimally commented, though it should be mostly clear what's going on from variable names. Really a lot can probablly be done to expand on that, as well as other areas.

For the interested, things I'm looking to outside of cleaning up the documentation are largely focused on finding a better way to cross-validate the scikit-learn models given that the data available is mostly going to be limited in number and subject to user-induced error. Also, there are a lot of issues involving getting the pyinstaller executable to actually play nice with the subprocess-spawning components of scikit-learn, right now they're just not inculuded, but I would like to find a way to get them to work without causing issues with the executable.

Outside of that, I'm happy to hear any suggestions that may be offered, so yeah. 
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

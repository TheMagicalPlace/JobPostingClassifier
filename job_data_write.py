import json
import os
import re
def json_to_text():
    goodj,badj = [job.name for job in os.scandir('Good_Jobs/')],[job.name for job in os.scandir('Bad Jobs/')]
    idealj,neutralj = [job.name for job in os.scandir('Ideal Jobs/')],[job.name for job in os.scandir('Neutral Jobs/')]
    with open(os.path.join(os.getcwd(),'jobs_data'),'r') as data:
        jobdat = json.loads(data.read())
    for jobsearchkey,job_desc in jobdat.items():
        try:
            os.mkdir(jobsearchkey)
        except FileExistsError:
            pass
        for key,info in job_desc.items():
            key = re.sub('/','|',key)
            if key in goodj or key in badj or key in neutralj or key in idealj:
                continue
            with open(f'{jobsearchkey}/{key}','w') as jobfile:
                for _,infodat in info.items():
                    jobfile.write(infodat)
                    jobfile.write('\n\n')



if __name__ == '__main__':
    json_to_text()
    print(len([e for e in os.scandir('Chemical Engineer/')]))
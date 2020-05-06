from scrapers import _scraper_template
import re
class ScraperIndeed(_scraper_template.ScraperBase):
    link_id = "jobtitle"
    job_id = "vjs-jobtitle"
    company_id = "vjs-cn"
    location_id = "vjs-loc"
    desc_id = "vjs-desc"

    def __init__(self,driver,database,search_term,no_of_calls,file_path_args=()):
        super().__init__(driver,database,search_term,no_of_calls=no_of_calls,file_path_args=file_path_args)
        self.seen = []


    def get_link(self,element):
        n = self.driver.find_element_by_id(self.job_id).text
        e = self.driver.find_elements_by_partial_link_text(n)
        if len(e) > 1:
            for lnk in e:
                lnk = lnk.get_attribute("href")
                if lnk in self.seen:
                    continue
                else:
                    self.seen.append(lnk)
                    link = lnk
                    break
        elif len(e) == 0:
            return "Link Not Found!"
        else:
            link = e[0].get_attribute("href")

        return link


    def get_job_name(self,*args):
        return self.driver.find_element_by_id("vjs-jobtitle").text

    def get_company_name(self,*args):
        return self.driver.find_element_by_id(self.company_id).text

    def get_job_location(self,*args):
        loc = self.driver.find_element_by_id(self.location_id).text,
        loc = re.sub(r'[-\'\\,]','',loc[0])
        return loc.strip()

    def get_description(self,*args):
        return self.driver.find_element_by_id(self.desc_id).text


    def get_post_date(self,*args):
        return ""





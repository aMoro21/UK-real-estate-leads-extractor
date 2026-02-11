from helper_functions import get_soup
import pandas as pd
import csv
from AgencyStructure import Agency
from AgenciesDatasExtractor import AgencyDataExtractor 
from AgenciesLinksExtractor import AgencyLinksExtractor 
import time 
from helper_functions import setup_logger
from os.path import exists

# setup logger 
logger = setup_logger(__name__)
class MainScraper: 
    def __init__(self):
        # the main data columns 
        self.file_headers = Agency.get_headers()
        self.main_url = 'https://www.yelu.uk/'

        self.current_url = ''
        self.csv_file = 'agencies_csv.csv'
        self.excel_file = 'UK_RealEstate_leads_data_sample.xlsx'
        self.log_file = 'scraper.log'
        self.page_limit = 25
        
    def get_leads_urls(self) : 
        """Returns the number of leads if file exists, else None ,Highly efficient line counting for large datasets."""
        existing_urls = set()
        if not exists(self.csv_file):
            return existing_urls
   
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get('source_url') # get the source url from each row 
                    if url:
                        existing_urls.add(url)
            
            logger.info(f"Detected {len(existing_urls)} existing leads in CSV.")
            return existing_urls
        except Exception as e:
            logger.error(f"Error reading existing CSV: {e}")
            return existing_urls 
    def run(self): 
        # check if the scraper has just started or it's been resumed 
        leads_urls = self.get_leads_urls()
        leads_count = len(leads_urls)
        if leads_count: 
            file_opening_mode = 'a'
            pages_scraped = leads_count // 20 
            logger.info(f'Scraper Resumed At Page {pages_scraped+1}')
        
        else:
            file_opening_mode = 'w'
            pages_scraped = 0 
            logger.info('Scraper Started') 
            # force clear the log file 
            open('scraper.log','w').close()


        current_page_num = pages_scraped + 1 
        self.current_url = AgencyLinksExtractor.build_next_page_url(self.main_url,current_page_num)
        
        with open(self.csv_file,file_opening_mode, newline='', encoding='utf-8') as f: 
            writer = csv.DictWriter(f, fieldnames=self.file_headers)
            if not(leads_urls) : writer.writeheader() # if that's the first time the file has been opened (The Scraper Has just Started)

            # to track pages 
            failed_page_links = 0 
        
            while current_page_num <= self.page_limit : 
                soup = self.handle_getting_soup(current_page_num)

                # If after the for-loop soup is None, handle the failure
                if not soup:
                    failed_page_links += 1
                    logger.error(f"Could not get soup for Page {current_page_num} after 3 attempts.")
                    
                    if failed_page_links >= 3:
                        logger.critical("Too many failed search pages. Stopping scraper to protect IP.")
                        break
                    
                    # Move to the next page using the manual static method
                    self.current_url = AgencyLinksExtractor.build_manual_url(self.main_url, current_page_num)
                    current_page_num += 1
                    continue # Skip the extraction part and jump to the next 'while' iteration

               
                failed_page_links = 0 # Reset failures because we captured a good page
                
                # get the agencies links from the page 
                links_extractor = AgencyLinksExtractor(soup,self.main_url)
                agencies_urls = links_extractor.get_all_urls()
                if not(agencies_urls): 
                    logger.error(f"Couldn't Find Page {current_page_num} Agencies Links, Continuing to the next page")
                    failed_page_links +=1 
                    if failed_page_links == 3 : 
                        logger.info('All Pages Have Been Scraped')
                        break

                    continue
                logger.info(f'Page {current_page_num} agencies links has been captured, Scraping Them Now')
                scraped_agencies = 0  
                to_scrape_urls = [url for url in agencies_urls if url not in leads_urls] # the urls remaining to finsih scraping this page 
                expected_urls = len(to_scrape_urls) # the number of them pages 
                # go through each agency url 
                for url in to_scrape_urls: 
                    # get the soup for the url for this agency 
                    agency_soup = get_soup(url)
                    if not(agency_soup): 
                        logger.warning(f"Couldn't Find Agency {url} soup")
                        # continue to the next agency 
                        time.sleep(0.5)
                        continue
                    # extract its data
                    data_extractor = AgencyDataExtractor(agency_soup)
                    agency_data_dict = data_extractor.all_data_extractor(url)
                    if not(agency_data_dict) : 
                        logger.warning(f"Couldn't Find Any Data to agency {url}")
                        time.sleep(0.5)
                        continue 
                    writer.writerow(agency_data_dict)
                    leads_urls.add(agency_data_dict['source_url'])
                    # to see the data while running
                    f.flush()
                    time.sleep(0.5)
                    scraped_agencies += 1
                # log the Number Of leads Extracted after each scraped page
                logger.info(f'+ {scraped_agencies} Scraped , Missing {expected_urls - scraped_agencies} agencies')
                self.current_url = links_extractor.get_next_url(current_page_num)
                current_page_num +=1 
        logger.info('Scraping Process Completed Succsesfuly')   

        '''This Function Returns A Finalized Report On How everything in the Scraper Went''' 
        pass   
    def convert_to_excel(self):
        try:
            # Load the CSV
            df = pd.read_csv(self.csv_file)
            # Save to Excel
            df.to_excel(self.excel_file, index=False)
            logger.info(f"Success! Saved {len(df)} agencies to {self.excel_file}")
        except Exception as e:
            logger.error(f"Excel conversion failed: {e}")
    def handle_getting_soup(self,current_page_num) : 
        '''This function trys to get the page soup for three times , returns soup or None'''
        for i in range(1, 4):
            soup = get_soup(self.current_url)
            if soup:
                return soup  # Return immediately on success
            
            logger.warning(f"Attempt {i}/3 failed for Page {current_page_num}. Retrying...")
            time.sleep(3)
        
        return None  # All attempts failed
    def finalize_scraper(self):
        if not exists(self.csv_file):
            logger.error("Report Failed: No data file found.")
            return

        try:
            df = pd.read_csv(self.csv_file)
            total_rows = len(df)
            
            if total_rows == 0:
                logger.warning("Integrity Report: No leads found to analyze.")
                return

            report_lines = [
                "", 
                "═" * 60,
                f"       FINAL DATA INTEGRITY REPORT ({time.strftime('%Y-%m-%d %H:%M')})",
                f"       Total Agencies Processed: {total_rows}",
                "═" * 60
            ]

            for column in df.columns:
                missing_count = df[column].isna().sum()
                success_rate = ((total_rows - missing_count) / total_rows) * 100
                
                # Logic: 100% = PASS, 95-99% = WARN, <95% = FAIL
                status = "✅ Pass" if success_rate == 100 else "⚠️  Warn" if success_rate > 95 else "❌ Fail"
                
                report_lines.append(f" {column.replace('_', ' ').title():<20} | Success: {success_rate:>6.2f}% | {status}")

            report_lines.append("═" * 60)
            logger.info("\n".join(report_lines))
            
        except Exception as e:
            logger.error(f"Integrity check failed: {e}")


def main() : 
    scraper = MainScraper()

    scraper.run()

    scraper.convert_to_excel()

    scraper.finalize_scraper()
    logger.info("Note: 'Website', 'Employees', and 'Establish Date' are sparse fields on Yelu.uk. Missing values reflect source data gaps, not extraction failures.")
if __name__ == '__main__' : 
    main()
# Description: Scraper for Huberman Lab Podcast
import os
import time
import logging
import uuid
from dataclasses import dataclass
from dataclasses import field

import pandas as pd
import requests
from tqdm.auto import tqdm
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

@dataclass
class Huberman:
    url: str = "https://www.hubermanlab.com/"
    episodes: list = field(default_factory=list)
    episode_data: list[dict] = field(default_factory=list)
    driver: webdriver.Chrome = field(default_factory=webdriver.Chrome)
    
    def __post_init__(self):
        """Initialize the class."""
        self.episodes = self.get_urls()
        self.episode_data = [self.get_episode_data(url) for url in tqdm(self.episodes, desc="Scraping Episodes")]
        self.records = self._build_dataframe(self.episodes, self.episode_data)
        
    @staticmethod
    def _chrome_options(*, headless: bool = False, user_agent: str = None):
        """Define the chrome options."""
        co = Options()
        ua = UserAgent()
        
        user_agent = ua.chrome if user_agent is None else user_agent
        co.add_experimental_option("excludeSwitches", ["enable-automation"])
        co.add_experimental_option("useAutomationExtension", False)
        co.add_argument(f"user-agent={user_agent}")
        if headless:
            co.add_argument("--headless=new")
        return co
    
    @staticmethod
    def _fetch_episode_urls(soup: BeautifulSoup):
        """Fetch the urls for each episode."""
        # all the episodes are in a div with the class name 'article-wrapper col'
        episodes_wrapper = soup.find_all("div", {"class": "article-wrapper col"})
        
        # inside the article-wrapper col, there is an 'article class' which contains the url
        episodes = [episode.find("article") for episode in episodes_wrapper]
        return [episode.find("a")["href"] for episode in episodes]
       
    def get_urls(self):
        """The webpage doesn't load all the episodes at once, so we need to scroll down to load more episodes."""
        # use selenium to scroll down the page
        self.driver.get(self.url)
        
        time.sleep(5)
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height

        # get the html
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        urls = self._fetch_episode_urls(soup)
        logger.info(f"Found {len(urls)} episodes")
        self.driver.close()
        
        return urls

    def get_episode_data(self, url: str) -> dict:
        """
        Each episode is on a separate page, so we need to scrap the data from each page.
        
        title = h1 class="entry-title"
        entry_content = div class "entry-content" in the <p> tags
        resources = any linked resources
        timestamps = h2 class=wp-block-heading id="h-timestamps
        
        """
        article = {}
        
        # use requests to get the html
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")
        
        # get the title
        try:
            article['title'] = soup.find("h1", {"class": "entry-title"}).text
        except AttributeError:
            article['title'] = None
            
        # get the entry content
        try:
            # the first p contains the links to social media. Skip this p
            paragraphs = soup.find("div", {"class": "entry-content"}).find_all("p")[1:]
            article['entry_content'] = [paragraph.text.strip() for paragraph in paragraphs]
        except AttributeError:
            article['entry_content'] = None
        
        # get the resource links: wp-block-heading id="h-resources"
        try:
            resources = soup.find("h2", {"id": "h-resources"}).find_next("ul").find_all("a")
            article['resources'] = [resource['href'] for resource in resources]
        except AttributeError:
            article['resources'] = None
            
        # get the timestamps: wp-block-heading id="h-timestamps"
        try:
            timestamps = soup.find("h2", {"id": "h-timestamps"}).find_next("ul").find_all("li")
            # get the timestamp links from the li
            article['timestamps'] = [timestamp.find("a")['href'] for timestamp in timestamps]
            # get the timestamp descriptions from the li text
            article['timestamp_descriptions'] = [timestamp.text.strip() for timestamp in timestamps]
        except AttributeError:
            article['timestamps'] = None
            article['timestamp_descriptions'] = None
            
        return article
        
    def _build_dataframe(self, episodes: list, episode_data: list[dict]) -> pd.DataFrame:
        """Construct the dataframe of the episode data"""
        
        ids = [uuid.uuid4() for _ in range(len(self.episodes))]
        
        episode_data = zip(ids, episodes, episode_data)
        
        df = pd.DataFrame(columns=['video_id', 'video_title',
                                   'video_description', 'video_url',
                                   'video_resources', 'timestamps',
                                   'timestamp_descriptions']
                          )
        
        # add the data to the dataframe
        for idx, episode, meta_data in episode_data:
            df.loc[len(df)] = [idx, meta_data['title'],
                                 meta_data['entry_content'], episode,
                                 meta_data['resources'], meta_data['timestamps'],
                                 meta_data['timestamp_descriptions']
                                ]
        
        return df

def _save_csv(df: pd.DataFrame, path: str):
    """Save the dataframe to a csv file."""
    logger.info(f"Saving data to {path}")
    
    # change the video description to semi-colon separated string
    df.records['video_description'] = df.records['video_description'].apply(lambda x: ' '.join(x) if x is not None else None)
    
    # change video resources to semi-colon separated string
    df.records['video_resources'] = df.records['video_resources'].apply(lambda x: '; '.join(x) if x is not None else None)
    
    # change timestamps to semi-colon separated string
    df.records['timestamps'] = df.records['timestamps'].apply(lambda x: '; '.join(x) if x is not None else None)
    
    # change timestamp descriptions to semi-colon separated string
    df.records['timestamp_descriptions'] = df.records['timestamp_descriptions'].apply(lambda x: '; '.join(x) if x is not None else None)
    
    # clean up for csv
    df.records.to_csv(f'{path}/video_metadata.csv', sep=',', quotechar='"', index=False)


def main():
    """Main function to control the Huberman Lab website to scrap the data for each episode.

    Raises:
        SystemExit: If the script fails to run.
    """
    huberman = Huberman()
    
    # make data dir
    if not os.path.exists('data'):
        logger.info('Creating data directory')
        os.makedirs('data')

    # save the data
    _save_csv(huberman, './data')
    
    
if __name__ == "__main__":
    raise SystemExit(main())

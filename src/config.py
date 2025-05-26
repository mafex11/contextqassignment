"""
Configuration file for the RSS feed scraper
"""

# Database configuration
DATABASE_PATH = "data/news.db"

# Scheduling configuration (in hours)
UPDATE_INTERVAL = 1

# RSS Feed sources
RSS_FEEDS = {
    "United Kingdom": [
        {
            "name": "BBC News",
            "url": "http://feeds.bbci.co.uk/news/rss.xml",
            "language": "en"
        },
        {
            "name": "The Guardian",
            "url": "https://www.theguardian.com/world/rss",
            "language": "en"
        }
    ],
    "United States": [
        {
            "name": "CNN",
            "url": "http://rss.cnn.com/rss/edition.rss",
            "language": "en"
        }
    ],
    "Japan": [
        {
            "name": "NHK World",
            "url": "https://www3.nhk.or.jp/rss/news/cat0.xml",
            "language": "ja"
        }
    ],
    "Qatar": [
        {
            "name": "Al Jazeera",
            "url": "https://www.aljazeera.com/xml/rss/all.xml",
            "language": "en"
        }
    ],
    "India": [
        {
            "name": "The Hindu Business Line",
            "url": "https://www.thehindubusinessline.com/news/?service=rss",
            "language": "en"
        },
        {
            "name": "The Hindu National",
            "url": "https://www.thehindu.com/news/national/?service=rss",
            "language": "en"
        }
    ],
    "Singapore": [
        {
            "name": "The Straits Times",
            "url": "https://www.straitstimes.com/news/world/rss.xml",
            "language": "en"
        }
    ],
    "Malaysia": [
        {
            "name": "The Star",
            "url": "https://www.thestar.com.my/rss/News",
            "language": "en"
        }
    ],
    "Australia": [
        {
            "name": "BBC Asia",
            "url": "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
            "language": "en"
        }
    ],
    "China": [
        {
            "name": "China Daily",
            "url": "https://www.chinadaily.com.cn/rss/world_rss.xml",
            "language": "en"
        }
    ],
    "France": [
        {
            "name": "Le Monde",
            "url": "https://www.lemonde.fr/en/rss/une.xml",
            "language": "fr"
        }
    ],
    "Brazil": [
        {
            "name": "CNN Brasil",
            "url": "https://admin.cnnbrasil.com.br/feed/",
            "language": "pt"
        }
    ],
    "Canada": [
        {
            "name": "CBC News",
            "url": "https://www.cbc.ca/webfeed/rss/rss-topstories",
            "language": "en"
        }
    ],
    "Denmark": [
        {
            "name": "BT",
            "url": "https://www.bt.dk/bt/seneste/rss",
            "language": "da"
        }
    ],
    "Egypt": [
        {
            "name": "Dialogue Across Borders",
            "url": "https://www.dialogueacrossborders.com/en/taxonomy/term/10896/feed",
            "language": "en"
        }
    ],
    "South Korea": [
        {
            "name": "Korea Herald",
            "url": "https://www.koreaherald.com/rss/",
            "language": "en"
        }
    ],
    "Indonesia": [
        {
            "name": "Jakarta Post",
            "url": "https://www.thejakartapost.com/rss/news",
            "language": "en"
        }
    ],
    "Thailand": [
        {
            "name": "Bangkok Post",
            "url": "https://www.bangkokpost.com/rss/data/news.xml",
            "language": "en"
        }
    ],
    "Philippines": [
        {
            "name": "Philippine Daily Inquirer",
            "url": "https://newsinfo.inquirer.net/feed",
            "language": "en"
        }
    ],
    "Vietnam": [
        {
            "name": "VnExpress International",
            "url": "https://e.vnexpress.net/rss/news.rss",
            "language": "en"
        }
    ],
    "Turkey": [
        {
            "name": "Daily Sabah",
            "url": "https://www.dailysabah.com/rss",
            "language": "en"
        }
    ],
    "Russia": [
        {
            "name": "RT News",
            "url": "https://www.rt.com/rss/",
            "language": "en"
        }
    ],
    "South Africa": [
        {
            "name": "News24",
            "url": "https://feeds.news24.com/articles/news24/TopStories/rss",
            "language": "en"
        }
    ],
    "Nigeria": [
        {
            "name": "Premium Times",
            "url": "https://www.premiumtimesng.com/feed",
            "language": "en"
        }
    ],
    "Mexico": [
        {
            "name": "Mexico News Daily",
            "url": "https://mexiconewsdaily.com/feed/",
            "language": "en"
        }
    ],
    "Argentina": [
        {
            "name": "Buenos Aires Herald",
            "url": "https://buenosairesherald.com/feed",
            "language": "en"
        }
    ],
    "Germany": [
        {
            "name": "Deutsche Welle",
            "url": "https://rss.dw.com/xml/rss-en-all",
            "language": "en"
        },
        {
            "name": "DW Germany",
            "url": "https://rss.dw.com/xml/rss-en-ger",
            "language": "en"
        }
    ],
    "Italy": [
        {
            "name": "ANSA English",
            "url": "https://www.ansa.it/english/news/general_news/rss.xml",
            "language": "en"
        }
    ],
    "Spain": [
        {
            "name": "El País English",
            "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/english.elpais.com/portada",
            "language": "en"
        }
    ],
    "Netherlands": [
        {
            "name": "Dutch News",
            "url": "https://www.dutchnews.nl/feed/",
            "language": "en"
        }
    ],
    "Sweden": [
        {
            "name": "The Local Sweden",
            "url": "https://www.thelocal.se/feed/",
            "language": "en"
        }
    ],
    "Norway": [
        {
            "name": "The Local Norway",
            "url": "https://www.thelocal.no/feed/",
            "language": "en"
        }
    ],
    "Finland": [
        {
            "name": "Yle News",
            "url": "https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET",
            "language": "en"
        }
    ],
    "Switzerland": [
        {
            "name": "SWI swissinfo.ch",
            "url": "https://www.swissinfo.ch/eng/latest/rss",
            "language": "en"
        }
    ],
    "Austria": [
        {
            "name": "The Local Austria",
            "url": "https://www.thelocal.at/feed/",
            "language": "en"
        }
    ],
    "Poland": [
        {
            "name": "The First News",
            "url": "https://www.thefirstnews.com/rss",
            "language": "en"
        }
    ],
    "Czech Republic": [
        {
            "name": "Prague Morning",
            "url": "https://praguemorning.cz/feed/",
            "language": "en"
        }
    ],
    "Greece": [
        {
            "name": "Ekathimerini",
            "url": "https://www.ekathimerini.com/rss",
            "language": "en"
        }
    ],
    "Portugal": [
        {
            "name": "The Portugal News",
            "url": "https://www.theportugalnews.com/rss",
            "language": "en"
        }
    ],
    "Ireland": [
        {
            "name": "The Irish Times",
            "url": "https://www.irishtimes.com/cmlink/news-1.1319192",
            "language": "en"
        }
    ],
    "Belgium": [
        {
            "name": "The Brussels Times",
            "url": "https://www.brusselstimes.com/feed",
            "language": "en"
        }
    ],
    "Israel": [
        {
            "name": "The Times of Israel",
            "url": "https://www.timesofisrael.com/feed/",
            "language": "en"
        }
    ],
    "United Arab Emirates": [
        {
            "name": "Gulf News",
            "url": "https://gulfnews.com/rss",
            "language": "en"
        }
    ],
    "Saudi Arabia": [
        {
            "name": "Arab News",
            "url": "https://www.arabnews.com/rss.xml",
            "language": "en"
        }
    ],
    "Iran": [
        {
            "name": "Press TV",
            "url": "https://www.presstv.ir/rss",
            "language": "en"
        }
    ],
    "Pakistan": [
        {
            "name": "Dawn",
            "url": "https://www.dawn.com/feeds/home",
            "language": "en"
        }
    ],
    "Bangladesh": [
        {
            "name": "The Daily Star",
            "url": "https://www.thedailystar.net/rss.xml",
            "language": "en"
        }
    ],
    "Sri Lanka": [
        {
            "name": "Daily Mirror",
            "url": "http://www.dailymirror.lk/RSS/",
            "language": "en"
        }
    ],
    "Nepal": [
        {
            "name": "The Kathmandu Post",
            "url": "https://kathmandupost.com/rss",
            "language": "en"
        }
    ],
    "Myanmar": [
        {
            "name": "Myanmar Times",
            "url": "https://www.mmtimes.com/rss.xml",
            "language": "en"
        }
    ],
    "Cambodia": [
        {
            "name": "Khmer Times",
            "url": "https://www.khmertimeskh.com/feed/",
            "language": "en"
        }
    ],
    "Laos": [
        {
            "name": "Vientiane Times",
            "url": "https://www.vientianetimes.org.la/rss.xml",
            "language": "en"
        }
    ],
    "New Zealand": [
        {
            "name": "Stuff.co.nz",
            "url": "https://www.stuff.co.nz/rss/",
            "language": "en"
        }
    ],
    "Kenya": [
        {
            "name": "The Star Kenya",
            "url": "https://www.the-star.co.ke/rss",
            "language": "en"
        }
    ],
    "Ghana": [
        {
            "name": "Ghana Web",
            "url": "https://www.ghanaweb.com/GhanaHomePage/rss/news.xml",
            "language": "en"
        }
    ],
    "Ethiopia": [
        {
            "name": "Ethiopian News Agency",
            "url": "https://www.ena.et/en/rss.xml",
            "language": "en"
        }
    ],
    "Morocco": [
        {
            "name": "Morocco World News",
            "url": "https://www.moroccoworldnews.com/feed/",
            "language": "en"
        }
    ],
    "Algeria": [
        {
            "name": "Algeria Press Service",
            "url": "https://www.aps.dz/en/rss",
            "language": "en"
        }
    ],
    "Tunisia": [
        {
            "name": "Tunisia Live",
            "url": "https://www.tunisialive.net/feed/",
            "language": "en"
        }
    ],
    "Chile": [
        {
            "name": "Santiago Times",
            "url": "https://santiagotimes.cl/feed/",
            "language": "en"
        }
    ],
    "Colombia": [
        {
            "name": "Colombia Reports",
            "url": "https://colombiareports.com/feed/",
            "language": "en"
        }
    ],
    "Peru": [
        {
            "name": "Peru Reports",
            "url": "https://perureports.com/feed/",
            "language": "en"
        }
    ],
    "Venezuela": [
        {
            "name": "Venezuela Analysis",
            "url": "https://venezuelanalysis.com/rss.xml",
            "language": "en"
        }
    ],
    "Ecuador": [
        {
            "name": "Ecuador Times",
            "url": "https://www.ecuadortimes.net/feed/",
            "language": "en"
        }
    ],
    "Uruguay": [
        {
            "name": "MercoPress",
            "url": "https://en.mercopress.com/rss.xml",
            "language": "en"
        }
    ],
    "Jamaica": [
        {
            "name": "Jamaica Observer",
            "url": "http://www.jamaicaobserver.com/rss/",
            "language": "en"
        }
    ],
    "Barbados": [
        {
            "name": "Barbados Today",
            "url": "https://barbadostoday.bb/feed/",
            "language": "en"
        }
    ],
    "Taiwan": [
        {
            "name": "Taiwan News",
            "url": "https://www.taiwannews.com.tw/rss",
            "language": "en"
        }
    ],
    "Hong Kong": [
        {
            "name": "Hong Kong Free Press",
            "url": "https://hongkongfp.com/feed/",
            "language": "en"
        }
    ],
    "Macao": [
        {
            "name": "Macau Daily Times",
            "url": "https://macaudailytimes.com.mo/feed",
            "language": "en"
        }
    ],
    "Mongolia": [
        {
            "name": "The UB Post",
            "url": "https://theubposts.com/feed/",
            "language": "en"
        }
    ],
    "Kazakhstan": [
        {
            "name": "The Astana Times",
            "url": "https://astanatimes.com/feed/",
            "language": "en"
        }
    ],
    "Uzbekistan": [
        {
            "name": "Uzbekistan Today",
            "url": "https://uzbekistan.lv/feed/",
            "language": "en"
        }
    ]
}

# Request headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Rate limiting configuration
REQUEST_DELAY = 1  # Delay between requests in seconds
MAX_RETRIES = 3    # Maximum number of retry attempts for failed requests

# Database table schema
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    publication_date TEXT NOT NULL,  -- Store as ISO format text to preserve timezone
    source TEXT NOT NULL,
    country TEXT NOT NULL,
    summary TEXT,
    url TEXT NOT NULL UNIQUE,
    language TEXT,
    created_at TEXT DEFAULT (datetime('now'))
)
""" 
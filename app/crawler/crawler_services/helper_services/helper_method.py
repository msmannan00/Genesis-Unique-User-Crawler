# Local Imports
from urllib.parse import urlparse
from gensim.parsing.preprocessing import STOPWORDS


class helper_method:

    # Extract URL Host
    @staticmethod
    def get_host_url(p_url):
        m_parsed_uri = urlparse(p_url)
        m_host_url = '{uri.scheme}://{uri.netloc}/'.format(uri=m_parsed_uri)
        if m_host_url.endswith("/"):
            m_host_url = m_host_url[:-1]
        return m_host_url

    # URL Cleaner
    @staticmethod
    def on_clean_url(p_url):
        if p_url.startswith("http://www.") or p_url.startswith("https://www.") or p_url.startswith("www."):
            p_url = p_url.replace("www.", "", 1)

        while p_url.endswith("/") or p_url.endswith(" "):
            p_url = p_url[:-1]

        return p_url

    # Remove Extra Slashes
    @staticmethod
    def normalize_slashes(p_url):
        p_url = str(p_url)
        segments = p_url.split('/')
        correct_segments = []
        for segment in segments:
            if segment != '':
                correct_segments.append(segment)
        normalized_url = '/'.join(correct_segments)
        normalized_url = normalized_url.replace("http:/", "http://")
        normalized_url = normalized_url.replace("https:/", "https://")
        normalized_url = normalized_url.replace("ftp:/", "ftp://")
        return normalized_url

    @staticmethod
    def is_stop_word(p_word):
        if p_word in STOPWORDS:
            return True
        else:
            return False

    @staticmethod
    def write_data(p_content, p_path):
        f = open(p_path.S_UNIQUE_HOST_FILE, "a")
        f.write(p_content + "\n")
        f.close()

    @staticmethod
    def sort_result(p_file):
        m_lines = []
        with open(p_file) as file:
            for line in file:
                m_lines.append(line.rstrip())
        m_lines.sort()
        with open(p_file, 'w') as f:
            for line in m_lines:
                f.write(f"{line}\n")

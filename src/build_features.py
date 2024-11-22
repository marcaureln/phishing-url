import os
import re
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.logging_config import get_logger

logger = get_logger('build_features')
logger.setLevel('INFO')


def is_ip(domain):
    """
        This regex will match any sequence of four numbers separated by dots. This is a simple way to check if a string is an IP address.)
        However, it doesn't strictly validate IP addresses. For example, it will match 999.999.999.999, which is not a valid IP address.
    """
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    value = bool(re.search(ip_pattern, domain))
    return int(value)


def char_con_rate(text):
    """
    Calculate the character continuation rate of a given text.

   The function is designed to assess the pattern of character repetition within a given text.
   It does this by identifying the longest consecutive sequences of characters, numbers, and special characters,
   and then calculating a weighted average of these sequences relative to the total length of the text.

    A higher rate indicates a greater presence of clustered character sequences,
    while a lower rate suggests a more dispersed distribution of characters.
    """
    rate = 0
    total_chars = len(text)
    max_char_count, max_num_count, max_special_count = 0, 0, 0
    current_char_count, current_num_count, current_special_count = 0, 0, 0

    for char in text:
        if char.isalpha():
            current_char_count += 1
            max_char_count = max(max_char_count, current_char_count)
            current_num_count, current_special_count = 0, 0
        elif char.isdigit():
            current_num_count += 1
            max_num_count = max(max_num_count, current_num_count)
            current_char_count, current_special_count = 0, 0
        else:
            current_special_count += 1
            max_special_count = max(max_special_count, current_special_count)
            current_char_count, current_num_count = 0, 0

        # Calculate the weighted average rate
        total_max_count = max_char_count + max_num_count + max_special_count
        rate = total_max_count / total_chars

    return rate


def no_of_subdomain(domain):
    """
    IP addresses are not domain names, thus they don't have subdomains.
    Subdomains are part of the DNS hierarchy and are only used in domain names.
    """
    if is_ip(domain):
        return 0

    domains = domain.split('.')
    return len(domains) - 2  # Subtract apex domain and TLD


def no_of_foo_in(string, pattern):
    """
    Counts the number of occurrences of a given pattern in a string.
    """
    # Find all matches of the pattern in the URL
    matches = re.findall(pattern, string)
    return len(matches)


def extract_domain(url):
    """
    Extracts the domain from a given URL.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Handle URLs without schemes
    if not domain:
        domain = url.split('/')[0]

        # Handle URLs with ports
        if ':' in domain:
            domain = domain.split(':')[0]

    return domain


def extract_feature(url):
    """
    Extracts features from a given URL.
    """
    domain = extract_domain(url)
    is_hostname_ip = is_ip(domain)

    if is_hostname_ip:
        return {
            'domain': domain,
            'domain_char_continuation_rate': None,
            'domain_length': len(domain),
            'is_ip': int(is_hostname_ip),
            'tld': None,
            'tld_length': None,
            'no_of_subdomain': 0,
            'no_of_letters': no_of_foo_in(url, r'[a-zA-Z]'),
            'letter_ratio': no_of_foo_in(url, r'[a-zA-Z]') / len(url),
            'no_of_digits': no_of_foo_in(url, r'\d'),
            'digit_ratio': no_of_foo_in(url, r'\d') / len(url),
            'is_https': int(False),
        }

    root_domain = domain.split('.')[-2]
    tld = domain.split('.')[-1]
    tld_length = len(tld)
    is_https = url.startswith('https://')

    return {
        'domain': domain,
        'domain_char_continuation_rate': char_con_rate(domain.split('.')[-2]),
        'domain_length': len(domain),
        'is_ip': int(is_hostname_ip),
        'tld': tld,
        'tld_length': tld_length,
        'no_of_subdomain': no_of_subdomain(domain),
        'no_of_letters': no_of_foo_in(root_domain, r'[a-zA-Z]'),
        'letter_ratio': no_of_foo_in(root_domain, r'[a-zA-Z]') / len(root_domain),
        'no_of_digits': no_of_foo_in(root_domain, r'\d'),
        'digit_ratio': no_of_foo_in(root_domain, r'\d') / len(root_domain),
        'is_https': int(is_https),
    }


def apply_extract_feature(row):
    """
    Apply the extract_feature function to each row of the DataFrame.
    """
    try:
        features = extract_feature(row['url'])
        new_row = row.to_dict()
        new_row.update(features)
    except Exception as e:
        logger.error(f"Error processing URL: {row['url']}, {e}")
        new_row = row.to_dict()
    return pd.Series(new_row)


if __name__ == "__main__":
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        logger.error("❌ DATABASE_URL is not set in the environment variables")
        exit(1)

    logger.info("🔌 Connecting to the database...")
    engine = create_engine(DATABASE_URL, connect_args={"options": "-c timezone=utc"})

    logger.info("💾 Loading data from the database...")
    df = pd.read_sql_table("url", engine, index_col="id")

    logger.info("🛠️ Extracting features from the URLs...")
    processed_df = df.apply(apply_extract_feature, axis=1)

    logger.info("🔄 Processing the data...")
    processed_df.drop(['source_id', 'is_online', 'created_at', 'updated_at'], axis=1, inplace=True)
    processed_df['is_phishing'] = processed_df['is_phishing'].astype(int)

    output_file = f'../data/data_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv'
    logger.info(f"📁 Saving processed data to {output_file}")
    processed_df.to_csv(output_file, index=False)

    logger.info("✅ Processing completed successfully")

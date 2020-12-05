from bs4 import BeautifulSoup

def get_relevant_html_tags(relevant_classes, soup):
    def is_any_class_match(css_class):
        if css_class is None:
            return False

        # sdap, profile, field, links, research, etc
        class_tokens =  set(re.split(r'\s|-', css_class.lower()))
        return len(class_tokens.intersection(key_classes_set)) > 0

    matches = []
    for match in soup.find_all(class_=is_any_class_match):
        matches = [m for m in matches if match not in m.descendants]
        matches.append(match)

    return matches

def extract_text_from_tags(tags):
    page_text = ' '.join([res.get_text(" ", strip=True) for res in tags])
    utf8_page_text = page_text.encode("ascii", errors="ignore").decode("utf-8")
    cleaned_page_text = re.sub("\s+", " ", utf8_page_text).strip()
    return cleaned_page_text

def extract_text_from_matching_tags(matching_classes, tags):
    # TODO
    matched_tags = []
    return extract_text_from_tags(matched_tags)

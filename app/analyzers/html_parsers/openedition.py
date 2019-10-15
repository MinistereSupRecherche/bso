from bs4 import BeautifulSoup
import re
from doi_utils import *


# doi 10.4000

def parse_openedition(soup):
    authors = []
    affiliations_complete= []

    is_french = False
    author_elts = soup.find("div", {"id":"authors"})
    if author_elts is None:
        author_elts = soup.find("div", {"id":"book-more-content-aboutauthor"})
    if author_elts is None:
        return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete':affiliations_complete}

    author_names = author_elts.find_all('h3')
    if len(author_names) == 0 :
        author_names = author_elts.find_all(class_='name')

    author_description_0 = author_elts.find_all(class_ = 'description')
    author_description = []
    for elt in author_description_0:
        if elt.find(class_="docnumber") is None:
            author_description.append(elt)


    if(len(author_names) != len(author_description) and len(author_names) > 1):
        associate_authors_affiliations = False
    else:
        associate_authors_affiliations = True

    for i, author_elt in enumerate(author_names):
        author={}

        last_name_elt = author_elt.find(class_= 'familyName')
        if last_name_elt:
            last_name = last_name_elt.get_text()
            first_name = author_elt.get_text().replace(last_name,'').strip()
            author['last_name'] = last_name
            author['first_name'] = first_name
        else:
            author['full_name'] = author_elt.get_text()

        if i<len(author_description):
            descriptions = re.split('–| ',author_description[i].get_text())
            structure_name, email = "", ""
            for e in descriptions:
                if '[at]' in e or '@' in e:
                    email  = e.replace('[at]', '@').strip()
                    if associate_authors_affiliations:
                        author['email'] = email
                else:
                    structure_name += e.strip()+' '
            if associate_authors_affiliations:
                author['affiliations_info'] = [{'structure_name':structure_name}]

            affiliations_complete.append({'structure_name':structure_name})

            if re.search(fr_regex, structure_name.lower()) or  re.search(fr_regex, email.lower()):
                is_french = True

        authors.append(author)

    return {'authors_from_html':authors, 'is_french':is_french, 'affiliations_complete': affiliations_complete}


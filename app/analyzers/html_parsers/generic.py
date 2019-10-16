import bs4
from bs4 import BeautifulSoup
import re
import datetime
from doi_utils import *
from app.utils.logger import create_logger

logger = create_logger(__name__)

affiliation_keywords = ['affiliation','affiliations','institution','institutions',\
                        'author','authors','country', 'auteur', 'auteurs', 'authoraffiliates', 'profile', 'affilia',\
                        'affiliationscontainer', 'contributors', 'contributor', 'authoraff', 'lblaffiliates', \
                        'affiliates', 'affiliate', 'scalex']
affiliation_regex = construct_regex(affiliation_keywords)
        
negative_match = "^_gaq|\(1[0-9][0-9]{2}|\(20[0-9]{2}|(;|,|\.).1[0-9][0-9]{2}|(;|,|\.).20[0-9]{2}|p\..[0-9]|^, «|France 2,|[0-9].p\.|^,.avec|resses universitaires|^,.catalogue|\(éd\.|par exemple|ibl\. |^,.éd\.|,.ed\.|,^Éd\.|^,(e|é|E|É)dit|^, et |il est |il a |notamment|, PUF|Dunod|Gallimard|Grasset|Hachette|Harmattan|Honoré Champion|Presses de|Larousse|Le Seuil|Albin Michel|Armand Collin|Belin|Belles Lettres|, (E|É)dition|Flammarion|Grasset|mprimerie|Karthala|La Découverte|Le Robert|Les Liens qui libèrent|Masson|Payot|Plon|Pocket|, Seuil|, Vrin|Odile Jacob|Fayard|^, thèse|(V|v)ol\.| eds\. |Octarès|Ellipses|Dalloz|Syros|^In |^(L|l)a |(L|l)es |logo cnrs|[0-9]{2}–[0-9]{2}| et al\.|Monod|National agreement in France|ovh-france|ar exemple|Pygmalion|Minuit|Puf|Karthala|^(P|p)our |^Presented|^(R|r)apport|^Reproducted from|^Revue|^Rev|^We thank|Zartman| price | VAT |^Support|^Sur |(S|s)pringer|^siècle|@|\.png|http|^(t|T)he |^\\n|^Does|(T|t)èse de"


def find_fr_affiliation (elt, verbose = False):
    if type(elt) == bs4.element.Tag:
        return find_fr_affiliation_elt(elt, verbose)
    #elif type(elt)==bs4.element.NavigableString:
    else:   
        return find_fr_affiliation_txt(elt, verbose)
    logger.debug ('error')
    logger.debug(type(elt))
    logger.debug(elt)
    return None


def find_fr_affiliation_elt(elt, verbose = False):
   

    is_fr = False
    affiliations = []

    forbidden_words = ['reference', 'http','bibliog']
    
    for att in elt.attrs:
        attribute_value = elt.attrs[att]

        if type(attribute_value)==str:
            attribute_value = attribute_value.lower()
        elif  type(attribute_value)==list:
            attribute_value = (" ".join(attribute_value)).lower()

        if 'title' in attribute_value.lower():
            return False, []

        for w in forbidden_words:
            if w in attribute_value or w in att.lower():
                return False, []

        if re.search(fr_regex, attribute_value):
            if(verbose):
                logger.debug('fr_kw in attribute value: ' + attribute_value)
            affiliations.append(attribute_value)
            is_fr = True

    if elt.findChildren()==[] and re.search(fr_regex, elt.get_text().lower()):
        if(verbose):
            logger.debug('fr_kw in elt - text: ' + elt.get_text().lower())
        affiliations.append(elt.get_text())
        is_fr = True

    return is_fr, list(set(affiliations))

def find_fr_affiliation_txt(elt, verbose = False):
    is_fr = False
    affiliations = []

#    for w in forbidden_words:
#        if w in elt.lower():
#            return False, []

    if re.search(fr_regex, elt.lower()):
        if(verbose):
            logger.debug('fr_kw in text: ' + elt.lower())
        affiliations.append(elt)
        is_fr = True

    return is_fr, list(set(affiliations))


def post_filter(x):
    affiliations_fr = x['affiliations_fr']
    affiliations_fr_filtered = []
    for e in affiliations_fr:
        if re.search(negative_match, e)==None and len(e)<250:
            affiliations_fr_filtered.append(e)

    is_french = (len(affiliations_fr_filtered) >0)
    return {'is_french':is_french, 'affiliations_fr':affiliations_fr_filtered}
 

def handler(signum, frame):
    logger.debug("Forever is over!")
    raise Exception("end of time")

def parse_generic(soup, verbose = False):

    #remove all options
    [x.extract() for x in soup.findAll('option')]
    [x.extract() for x in soup.findAll('title')]
    [x.extract() for x in soup.findAll(class_ = 'fig-caption')]
    [x.extract() for x in soup.findAll(class_ = 'materials-methods')]
    [x.extract() for x in soup.findAll(class_ = 'toc-section')]


    is_french=False
    all_affiliations=[]

    possible_elts = [e for e in soup.descendants if type(e)==bs4.element.Tag]
    if(possible_elts == []):
        return {'is_french': is_french, 'affiliations_fr':all_affiliations}

    try:

        elt_to_check = []
        for elt in possible_elts:
            is_affiliation_elt = False

            if elt==None:
                continue
            
            
            if len(elt.findChildren())==0 and re.search(affiliation_regex, elt.get_text().lower()):
                is_affiliation_elt = True
                if(verbose):
                    logger.debug('kw 1 affiliation in '+ elt.get_text().lower())
                
            for sub_elt in elt.findChildren():
                if sub_elt.find('sup'):
                    is_affiliation_elt = True
                    if(verbose):
                        logger.debug('kw sup affiliation in '+ elt.get_text().lower())

                
            for att in elt.attrs:
                attribute_value = elt.attrs[att]
                if type(attribute_value)==str:
                    attribute_value = attribute_value.lower()
                elif  type(attribute_value)==list:
                    attribute_value = (" ".join(attribute_value)).lower()

                if re.search(affiliation_regex, att.lower()) or re.search(affiliation_regex, attribute_value):
                        is_affiliation_elt = True
                        if(verbose):
                            logger.debug('*********************')
                            logger.debug('kw2 affiliation in ')
                            logger.debug(att.lower())
                            logger.debug(attribute_value)
                            logger.debug('*********************')


            if(is_affiliation_elt):
                elt_to_check.append(elt)
                elt_to_check += [e for e in elt.descendants]
 
        all_affiliations = []
    
        for elt in list(set(elt_to_check)):
            is_french, affiliations = find_fr_affiliation(elt, verbose)
            if is_french:
                all_affiliations += affiliations

        all_affiliations = list(set(all_affiliations))
    
        if len(all_affiliations) > 0:
            is_french = True
        else:
            is_french = False

    except:
        pass
    
    return post_filter({'is_french': is_french, 'affiliations_fr':all_affiliations})


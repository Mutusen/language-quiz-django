import urllib3, json
from django.utils import translation


def get_wikipedia_link(language_code):
    http = urllib3.PoolManager()
    # Step 1: get the Wikidata ID of the language from the English Wikipedia
    url = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&format=json&titles=ISO_639:' + language_code
    r = http.request('GET', url)
    json_data = json.loads(r.data)
    pages = json_data['query']['pages']
    key = list(pages.keys())[0]
    wikidata_id = pages[key]['pageprops']['wikibase_item']

    # Step 2: get translations of the article from Wikidata
    url = 'https://www.wikidata.org/wiki/Special:EntityData/' + wikidata_id + '.json'
    r = http.request('GET', url)
    json_data = json.loads(r.data)

    requested_wiki_code = translation.get_language() + "wiki"  # e.g. frwiki if the user is using the French version
    sitelinks = json_data['entities'][wikidata_id]['sitelinks']
    if requested_wiki_code in sitelinks.keys():
        wikiurl = sitelinks[requested_wiki_code]['url']
    else:
        wikiurl = sitelinks['enwiki']['url']

    return wikiurl

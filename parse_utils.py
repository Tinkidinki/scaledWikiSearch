import re
'''If the following functions are used, please call them in the order they are written here'''

def get_infobox(s):
    infobox_text = ""
    re_func = re.compile(r'(\{\{Infobox(.|\n)*?\}\}\n)(?:[^\|])')
    infobox_temp = re_func.search(s)
    if (infobox_temp):
        infobox_text = infobox_temp.group(1)
        s = s.replace(infobox_text, "")
    infobox_text = infobox_text.replace("Infobox", " ")
    return (s, infobox_text)

def get_categories(s):
    category_text = ""
    re_func = re.compile(r'\[\[Category.*?\]\]')
    categories = re_func.findall(s)
    category_text = ' '.join(categories)
    for cat in categories:
        s = s.replace(cat, "")
    category_text = category_text.replace("Category:", " ")
    return (s, category_text)

def get_links(s):
    link_text = ""
    re_func = re.compile(r'==External links==(.|\n)*')
    links_temp = re_func.search(s)
    if (links_temp):
        link_text = links_temp.group()
        s = s.replace(link_text, "")
    link_text = link_text.replace("==External links==", " ")
    return (s, link_text)

def get_refs(s):
    ref_text = ""
    re_func = re.compile(r'==References==(.|\n)*')
    refs_temp = re_func.search(s)
    if (refs_temp):
        ref_text = refs_temp.group()
        s = s.replace(ref_text, "")
    ref_text = ref_text.replace("==References==", " ")
    return (s, ref_text)

    


    
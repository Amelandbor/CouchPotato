from string import ascii_letters, digits
import re
import unicodedata
import xml.etree.ElementTree as XMLTree

class rss:

    timeout = 10

    def toSaveString(self, string):
        string = self.latinToAscii(string)
        string = ''.join((c for c in unicodedata.normalize('NFD', unicode(string)) if unicodedata.category(c) != 'Mn'))
        safe_chars = ascii_letters + digits + '_ -.,\':!?'
        r = ''.join([char if char in safe_chars else ' ' for char in string])
        return re.sub('\s+' , ' ', r)

    def toSearchString(self, string):
        string = self.latinToAscii(string)
        string = ''.join((c for c in unicodedata.normalize('NFD', unicode(string)) if unicodedata.category(c) != 'Mn'))
        safe_chars = ascii_letters + digits + ' \''
        r = ''.join([char if char in safe_chars else ' ' for char in string])
        return re.sub('\s+' , ' ', r).replace('\'s', 's').replace('\'', ' ')

    def latinToAscii(self, unicrap):
        xlate = {0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
            0xc6:'Ae', 0xc7:'C',
            0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E', 0x86:'e',
            0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
            0xd0:'Th', 0xd1:'N',
            0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
            0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
            0xdd:'Y', 0xde:'th', 0xdf:'ss',
            0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
            0xe6:'ae', 0xe7:'c',
            0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
            0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
            0xf0:'th', 0xf1:'n',
            0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
            0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
            0xfd:'y', 0xfe:'th', 0xff:'y',
            0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
            0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
            0xa9:'{C}', 0xaa:'{^a}', 0xab:'<<', 0xac:'{not}',
            0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
            0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
            0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
            0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>',
            0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'?',
            0xd7:'*', 0xf7:'/'
            }

        r = ''
        for i in unicrap:
            if xlate.has_key(ord(i)):
                r += xlate[ord(i)]
            elif ord(i) >= 0x80:
                pass
            else:
                r += str(i)
        return r


    def gettextelements(self, xml, path):
        ''' Find elements and return tree'''

        textelements = []
        try:
            elements = xml.findall(path)
        except:
            return
        for element in elements:
            textelements.append(element.text)
        return textelements

    def gettextelement(self, xml, path):
        ''' Find element and return text'''

        try:
            return xml.find(path).text
        except:
            return

    def getItems(self, data, path = 'channel/item'):
        return XMLTree.parse(data).findall(path)

    class feedItem(dict):
        ''' NZB item '''

        def __getattr__(self, attr):
            return self.get(attr, None)

        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

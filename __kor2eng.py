BASE_CODE, CHO_CODE, JUNG_CODE, MAX_CODE = 44032, 588, 28, 55203
CHO_LIST = list('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
JUNG_LIST = list('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
JONG_LIST = list(' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')

KORS = list('ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
ENGS = ['r', 'R', 'rt', 's', 'sw', 'sg', 'e', 'f', 'fr', 'fa', 'fq', 'ft', 'fx', 'fv', 'fg', 'a', 'q', 'qt', 't',
        'T', 'd', 'w', 'c', 'z', 'x', 'v', 'g',
        'k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk', 'ho', 'hl', 'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l']
KOR_ENG_TABLE = dict(zip(KORS, ENGS))

def kor2eng(text):
    res = ''
    for ch in text:
        spl = split(ch)
        if spl is None:
            res += ch
            continue
        
        for kr in spl:
            en = None
            if kr in KOR_ENG_TABLE:
                en = KOR_ENG_TABLE[kr]

            if en is not None:
                res += en
    return res


def combine(cho, jung, jong):
    res = BASE_CODE
    res += 0 if cho == ' ' else CHO_LIST.index(cho) * CHO_CODE
    res += 0 if jung == ' ' else JUNG_LIST.index(jung) * JUNG_CODE
    res += JONG_LIST.index(jong)
    return chr(res)


def split(kor):
    code = ord(kor) - BASE_CODE
    if code < 0 or code > MAX_CODE - BASE_CODE:
        if kor == ' ': return None
        if kor in CHO_LIST: return kor, ' ', ' '
        if kor in JUNG_LIST: return ' ', kor, ' '
        if kor in JONG_LIST: return ' ', ' ', kor
        return None
    return CHO_LIST[code // CHO_CODE], JUNG_LIST[(code % CHO_CODE) // JUNG_CODE], JONG_LIST[(code % CHO_CODE) % JUNG_CODE]

def SplitByKorEng(str):
    list = []

    lang = ""
    prev_lang = ""
    str_temp = ""
    for c in str:
        prev_lang = lang
        if ord('가') <= ord(c) <= ord("힇"):
            lang = "kr"
        elif ord('a') <= ord(c) <= ord("z") or ord('A') <= ord(c) <= ord("Z"):
            lang = "en"

        if prev_lang != "" and prev_lang != lang:
            list.append((str_temp, prev_lang))
            str_temp = ""

        str_temp += c

    list.append((str_temp, lang))
    return list
    
if __name__ == '__main__':
    str = "Velhakana"
    print(str)
    print(*SplitByKorEng(str), sep="\n")
import pyautogui as pag
import pywinauto
import pygetwindow as gw
import __MentionMaker
import time
import __kor2eng
import sys
import datetime
from functools import reduce

PRESS_DEBUG = False
MENTION_DEBUG = False
KATALK_DEBUG = False
EXPORT_TODAY = False

def SpreadName2KakaoName(spread_name):
    if spread_name == "예토":
        return "예토"
    elif spread_name == "벸":
        return "벸"
    elif spread_name == "아이티":
        return "EyeT"
    elif spread_name == "푸바":
        return "푸른바람"
    elif spread_name == "꿈방":
        return "꿈방"
    elif spread_name == "아카":
        return "웨총탕총탕"
    elif spread_name == "Art":
        return "Art"
    elif spread_name == "라비에몽":
        return "Lavienus"
    elif spread_name == "상어":
        return "상어is상어"
    elif spread_name == "빡상":
        return "카마인섭이고픈박쌍혁"
    elif spread_name == "구뱅":
        return "틀서커(진) 구뱅"
    elif spread_name == "말랑":
        return "말랑카우블랙"
    elif spread_name == "분니":
        return "분니수거"
    elif spread_name == "사슴":
        return "산속숲속숫사슴"
    elif spread_name == "정별":
        return "정별"
    elif spread_name == "외않되":
        return "기술슼인생낭비"
    elif spread_name == "푸스":
        return "Velhakana"
    elif spread_name == "사다":
        return "사다하루"
    elif spread_name == "약좀":
        return "약한좀비"
    elif spread_name == "현지":
        return "우주미누"
    elif spread_name == "온세상":
        return "온세상"
    elif spread_name == "수상":
        return "예비역 수상한 뱁새"
        
    return "오류"

def press(string, lang="kr"):
    if PRESS_DEBUG == True:
        print(string)
        return 

    if string == "sh_enter":
        pag.hotkey("shift", "enter")
        return
    if string == "enter":
        pag.press("enter")
        return

    if lang == "en":
        pag.hotkey('hanguel')

    pag.write(__kor2eng.kor2eng(string))

    if lang == "en":
        pag.hotkey('hanguel')

def mention(splited_str):
    if PRESS_DEBUG == True:
        print(reduce(lambda x: x[0], splited_str))
        return 

    if len(splited_str) == 1 and splited_str[0][0] == "오류":
        pag.write(splited_str[0][0] + " ")

    pag.write("@")
    time.sleep(0.2)
    for splited in splited_str:
        string, lang = splited

        if lang == "en":
            pag.hotkey('hanguel')

        pag.write(__kor2eng.kor2eng(string))
            
        if lang == "en":
            pag.hotkey('hanguel')

    time.sleep(0.2)

    if MENTION_DEBUG == False:
        pag.press("enter")
    else:
        pag.press(" ")


if __name__ == "__main__":
    for rgv in sys.argv:
        if rgv == "/MENTION_DEBUG":
            MENTION_DEBUG = True
        if rgv == "/KATALK_DEBUG":
            KATALK_DEBUG = True
        if rgv == "/PRESS_DEBUG":
            PRESS_DEBUG = True
        if rgv == "/TABLE_DEBUG":
            __MentionMaker.TABLEDATA_DEBUG = True
        if rgv == "/EXPORT_TODAY":
            EXPORT_TODAY = True

    katalk_title = ""
    if KATALK_DEBUG == True:
        katalk_title = "박유진"
    else:
        katalk_title = "팀노블 스케줄"

    alert_str = """1. \"{0}\" 카톡방을 열어두세요.
2. 카톡방 대화 입력 칸 클릭 후, 한글로 써지는걸 확인하고 "확인"을 누르세요.
확인 안하면 한/영 반대로 나오게 됩니다.
3. 출력 중 다른 행동을 하지 말아주세요. 중간에 나오다 끊길 수 있습니다.
""".format(katalk_title)
    if pag.confirm(alert_str) != "OK":
        quit()

    win_list = gw.getWindowsWithTitle(katalk_title)
    if len(win_list) == 0:
        pag.alert("{0} 카톡창을 찾을 수 없습니다.".format(katalk_title))
        quit()

    win = win_list[0]
    if win.isActive == False:
        pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
    win.activate()

    print("로프레드시트 테이블 데이터 파싱 중...", end=" ")
    TableMaker = __MentionMaker.MentionMaker()
    TableData = TableMaker.GetTableData()
    print("완료 !")
    
    time.sleep(1)
    print("카카오톡 자동 입력 진행 중...", end=" ")

    str_pre = ""
    for_range = []
    if EXPORT_TODAY == True:
        Weekday_int = datetime.datetime.today().weekday()
        Weekday_int -= 2
        if Weekday_int < 0:
            Weekday_int += 7
        for_range = range(Weekday_int,Weekday_int+1)
        str_pre = "오늘의 일정 보내드립니다."
    else:
        for_range = range(0,7)
        str_pre = "이번주 일정 보내드립니다."

    win.activate()
    press(str_pre)
    press("enter")

    for i in for_range:
        if i not in TableData:
            continue

        Contents_List = TableData[i]
        Weekday = __MentionMaker.GetWeekdayByPriority(i)

        press(Weekday)
        press("sh_enter")

        size = len(Contents_List)
        player_counter = 0
        for i in range(size):
            Contents = Contents_List[i]
            
            Time = Contents[0]
            Party = Contents[1]

            player_counter += len(Party)
            
            press(Time)
            press("sh_enter")
            
            for Player in Party:
                kakao_nickname = SpreadName2KakaoName(Player)
                mention(__kor2eng.SplitByKorEng(kakao_nickname))
                time.sleep(0.3)

            if (8-len(Party)) % 4 != 0:
                press(("+ 공석 {0}".format((8-len(Party)) % 4)))

            if i == size - 1:
                press("enter")
            else:
                if player_counter + len(Contents_List[i+1][1]) > 15:
                    player_counter = 0
                    press("enter")

                    press(Weekday)
                    press("sh_enter")
                else:
                    press("sh_enter")
                    press("sh_enter")
            
    press("enter")
    press("이상입니다. 감사합니다.")
    press("enter")

    print("완료 !")
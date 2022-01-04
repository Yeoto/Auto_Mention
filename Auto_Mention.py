import pyautogui as pag
import pywinauto
import pygetwindow as gw
import __MentionMaker
import time
import __kor2eng
import sys
import datetime

PRESS_DEBUG = False
MENTION_DEBUG = False
KATALK_DEBUG = False
EXPORT_TODAY = False

def SpreadName2KakaoName(spread_name):
    if spread_name == "예토":
        return (__kor2eng.kor2eng("예토"), "kr")
    elif spread_name == "벸":
        return (__kor2eng.kor2eng("벸"), "kr")
    elif spread_name == "아이티":
        return ("EyeT", "en")
    elif spread_name == "푸바":
        return (__kor2eng.kor2eng("푸른바람"), "kr")
    elif spread_name == "꿈방":
        return (__kor2eng.kor2eng("꿈방"), "kr")
    elif spread_name == "아카":
        return (__kor2eng.kor2eng("웨총탕총탕"), "kr")
    elif spread_name == "Art":
        return ("Art", "en")
    elif spread_name == "라비에몽":
        return ("Lavienus", "en")
    elif spread_name == "상어":
        return (__kor2eng.kor2eng("홀리가된상어/카마인/도우미"), "kr")
    elif spread_name == "빡상":
        return (__kor2eng.kor2eng("카마인섭이고픈박쌍혁"), "kr")
    elif spread_name == "구뱅":
        return (__kor2eng.kor2eng("틀서커(진) 구뱅"), "kr")
    elif spread_name == "말랑":
        return (__kor2eng.kor2eng("말랑카우블랙"), "kr")
    elif spread_name == "분니":
        return (__kor2eng.kor2eng("분니수거"), "kr")
    elif spread_name == "사슴":
        return (__kor2eng.kor2eng("산속숲속숫사슴"), "kr")
    elif spread_name == "정별":
        return (__kor2eng.kor2eng("정별"), "kr")
    elif spread_name == "외않되":
        return (__kor2eng.kor2eng("기술슼인생낭비"), "kr")
    elif spread_name == "푸스":
        return ("Velhakana", "en")
    elif spread_name == "사다":
        return (__kor2eng.kor2eng("사다하루"), "kr")
    elif spread_name == "약좀":
        return (__kor2eng.kor2eng("약한좀비"), "kr")
    elif spread_name == "현지":
        return (__kor2eng.kor2eng("우주미누"), "kr")
    elif spread_name == "온세상":
        return (__kor2eng.kor2eng("온세상"), "kr")
        
    return (__kor2eng.kor2eng("오류"), "kr")

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

    pag.write(string)

    if lang == "en":
        pag.hotkey('hanguel')

def mention(string, lang):
    if PRESS_DEBUG == True:
        print(string)
        return 

    if MENTION_DEBUG == True:
        press("@" + string + " ", lang)
        return

    if lang == "en":
        pag.hotkey('hanguel')

    if string != __kor2eng.kor2eng("오류"):
        temp_string = "@" + string
        pag.write(temp_string)
        time.sleep(0.2)
        pag.press("enter")
    else:
        pag.write(string + " ")
        
    if lang == "en":
        pag.hotkey('hanguel')


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
    press(__kor2eng.kor2eng(str_pre))
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
            
            press(__kor2eng.kor2eng(Time))
            press("sh_enter")
            
            for Player in Party:
                kakao_nickname = SpreadName2KakaoName(Player)
                mention(kakao_nickname[0], kakao_nickname[1])
                time.sleep(0.3)

            if (8-len(Party)) % 4 != 0:
                press(__kor2eng.kor2eng("+ 공석 {0}".format((8-len(Party)) % 4)))

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
    press(__kor2eng.kor2eng("이상입니다. 감사합니다."))
    press("enter")

    print("완료 !")
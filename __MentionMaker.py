import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

TABLEDATA_DEBUG = False

def GetWeekdayPriorityByWeekday(Weekday):
    if Weekday == "수":
        return 0
    elif Weekday == "목":
        return 1
    elif Weekday == "금":
        return 2
    elif Weekday == "토":
        return 3
    elif Weekday == "일":
        return 4
    elif Weekday == "월":
        return 5
    elif Weekday == "화":
        return 6

    return -1

def GetWeekdayByPriority(Priority):
    if Priority == 0:
        return "tn"
    elif Priority == 1:
        return "ahr"
    elif Priority == 2:
        return "rma"
    elif Priority == 3:
        return "xh"
    elif Priority == 4:
        return "dlf"
    elif Priority == 5:
        return "dnjf"
    elif Priority == 6:
        return "ghk"

    return ""

class MentionMaker:
    #TableData = { 월 : [(컨텐츠+시간, [player1, ..., player8])],  
    #              화 : ..., }
    TableData = {}
    KaTalk_Dict = {}

    def __init__(self):
        self.LoadParsingData()
        return

    def LoadParsingData(self):
        scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

        json_file_name = 'lostark-metionmaker-f6d9d056e6ca.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)

        gc = gspread.authorize(credentials)
        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1evS2wYW3Lss8vI_cHUyB7VjRV9yVvOj8XnK8Yj8nKtQ'

        # 스프레스시트 문서 가져오기 
        doc = gc.open_by_url(spreadsheet_url)

        # 시트 선택하기
        worksheet = doc.worksheet('공대장용_구성예정파티_원정대')

        range_list = []

        if TABLEDATA_DEBUG == True:
            range_list = worksheet.range("B3:B3")
        else:
            range_list = worksheet.range("B3:B70")

        #뭔가.. 가져오는데 버그가 있는듯..;; 일단 한번 읽고 10초 대기시켜서 로딩되도록 함
        row_cells = worksheet.row_values(1)
        time.sleep(10)

        for cell in range_list:
            if cell.value != 'O':
                continue

            row_cells = worksheet.row_values(cell.row)

            if len(row_cells) < 20:
                continue

            Weekday = GetWeekdayPriorityByWeekday(row_cells[3][0:1])
            Contents = row_cells[2]

            Contents = Contents.replace("N", " 노말")
            Contents = Contents.replace("H", " 하드")

            Contents_Time = Contents + " " + row_cells[3][2:]
            Party = []
            for i in range(21, 29):
                if i >= len(row_cells):
                    break
                if row_cells[i] != "":
                    Party.append(row_cells[i])

            if Weekday not in self.TableData:
                self.TableData[Weekday] = []

            self.TableData[Weekday].append((Contents_Time, Party))

        for i in range(0,7):
            if i not in self.TableData:
                continue
            
            self.TableData[i].sort(key = lambda x: int(x[0][-5:].replace(":","").replace("++","01")))

        worksheet = doc.worksheet('원정대 시트')
        datas_katalk = worksheet.row_values(1)
        datas_basenick = worksheet.row_values(2)
        
        self.KaTalk_Dict = dict(zip(datas_basenick, datas_katalk))
        return

    def PrintTableData(self):
        for i in range(0,7):
            if i not in self.TableData:
                continue

            Contents_List = self.TableData[i]
            Weekday = GetWeekdayByPriority(i)

            print(Weekday)
            for Contents in Contents_List:
                Time = Contents[0]
                Party = Contents[1]
                Party_str = " ".join(Party)
                print(Time)
                print(Party_str)
                print()
            print()
        return
        
    def GetTableData(self):
        return self.TableData, self.KaTalk_Dict
   

if __name__ == "__main__":
    TableMaker = MentionMaker()
    TableMaker.PrintTableData()
import requests
from datetime import datetime, timezone, timedelta
from ics import Calendar, Event


## 节日日历，包含当年及下一年的节日

def festival_events():
    current_year = datetime.now().year
    next_year = datetime.now().year + 1

    ## 如果假日日历中已经包含的节日，维护时需要注意不要在此处添加
    care_festival_name = ['元宵节', '情人节', '妇女节', '愚人节', '母亲节', '儿童节', '父亲节', '七夕节', '中元节',
                          '万圣节', '圣诞节', '平安夜']
    care_festival_event = []
    festival_json_url = f"https://raw.githubusercontent.com/zqzess/openApiData/refs/heads/main/calendar_new/{current_year}/{current_year}.json"
    next_festival_json_url = f"https://raw.githubusercontent.com/zqzess/openApiData/refs/heads/main/calendar_new/{next_year}/{next_year}.json"

    festival_json = requests.get(festival_json_url).json() + requests.get(next_festival_json_url).json()
    for month in festival_json:
        for entry in month.get('almanac'):
            for festival_info in entry.get('festivalInfoList', []):
                if festival_info['name'] in care_festival_name:
                    date = datetime.fromtimestamp(int(entry['timestamp']))
                    e = Event(name=festival_info['name'], begin=date, end=date)
                    e.make_all_day()
                    care_festival_event.append(e)
    return care_festival_event


## 假日日历格式整理
def holiday_events_fixup(events):
    for event in events:
        # 清除所有补班的alarm提醒
        event.alarms = []

        # 设置为全天日程，防止UTC时间漂移
        event.make_all_day()

        # 日历标题简化，提示班or休
        name = event.name.split(' ')
        new_name = ('(班)' if name[1] == '补班' else '(休)') +name[0]
        event.name = new_name

def main():
    holiday_ics_url = 'https://raw.githubusercontent.com/lanceliao/china-holiday-calender/refs/heads/master/holidayCal.ics'

    calendar = Calendar(requests.get(holiday_ics_url).text)

    holiday_events_fixup(calendar.events)

    events = festival_events()
    for event in events:
        calendar.events.add(event)

    with open('holiday_festival_cal.ics', 'w', encoding='utf-8') as f:
        f.writelines(calendar.serialize_iter())


if __name__ == '__main__':
    main()

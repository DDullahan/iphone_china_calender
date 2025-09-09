import requests
from datetime import datetime
from ics import Calendar, Event


def festival_events():
    current_year = datetime.now().year
    care_festival_name = ['元宵节', '情人节', '妇女节',   '愚人节', '清明','劳动节','元旦','除夕','春节','母亲节','端午节','儿童节','父亲节','七夕节', '中元节','国庆节','万圣节','圣诞节','平安夜']
    care_festival_event = []
    festival_json_url = f"https://raw.githubusercontent.com/zqzess/openApiData/refs/heads/main/calendar_new/{current_year}/{current_year}.json"
    festival_json = requests.get(festival_json_url).json()

    for month in festival_json:
        for entry in month.get('almanac'):
            for festival_info in entry.get('festivalInfoList', []):
                if festival_info['name'] in care_festival_name:
                    date = datetime.fromtimestamp(int(entry['timestamp']))
                    e = Event(name=festival_info['name'], begin=date, end=date)
                    e.make_all_day()
                    care_festival_event.append(e)
    return care_festival_event




def main():
    holiday_ics_url = 'https://raw.githubusercontent.com/lanceliao/china-holiday-calender/refs/heads/master/holidayCal.ics'

    calendar = Calendar(requests.get(holiday_ics_url).text)

    events = festival_events()
    for event in events:
        calendar.events.add(event)

    with open('holiday_festival_cal.ics', 'w', encoding='utf-8') as f:
        f.writelines(calendar.serialize_iter())

if __name__ == '__main__':
    main()
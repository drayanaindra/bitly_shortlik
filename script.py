import requests, json, csv

url = "https://api-ssl.bitly.com/v4/shorten"
url_custom = "https://api-ssl.bitly.com/v4/custom_bitlinks"
headers = {
    'Authorization': 'Bearer {TOKEN}', 
    'Content-Type': 'application/json'
}

origin_csv = 'file.csv'
new_csv = 'file_new.csv'
group_id = "GROUP_ID"

def create_short_link():
    header_new_csv = ['school', 'pic', 'city', 'originlink', 'shortlink']
    csv_data = []

    with open(origin_csv, 'rb') as f:
        for i, line in enumerate(f):
            if i > 0:
                raw_data = str(line.split()[0], 'utf-8')
                get_school = raw_data.split(",")[0]
                get_pic = raw_data.split(",")[1]
                get_city = raw_data.split(",")[2]
                get_classcode = raw_data.split(",")[3]
                get_originlink = raw_data.split(",")[4]
                cust_link = "bit.ly/"+get_school

                data_for_shortlink = {
                    "long_url": get_originlink,
                    "domain": "bit.ly",
                    "group_guid": group_id,
                }

                res = requests.post(url, headers=headers, json=data_for_shortlink)
                res_to_json_shorlink = json.loads(res.text)

                data_cust_backhalf = {
                    "custom_bitlink": cust_link,
                    "bitlink_id": res_to_json_shorlink.get("id")
                }

                custom_backhalf = requests.post(url_custom, headers=headers, json=data_cust_backhalf)
                res_to_json_backhalf = json.loads(custom_backhalf.text)
                custom_short_link = res_to_json_backhalf.get("custom_bitlink")

                csv_data.append([get_school, get_pic, get_city, get_classcode, get_originlink, custom_short_link])

    with open(new_csv, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header_new_csv)
        writer.writerows(csv_data)


create_short_link()
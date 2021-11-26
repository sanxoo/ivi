import csv

def save(info, items):
    with open(info["file"], "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(info["keys"])
        for item in items:
            row = [item[key] for key in info["keys"]]
            writer.writerow(row)
        
if __name__ == "__main__":
    items = [
        {'baekduId': 'BAEK_31', 'baekdudistance': '6.1㎞', 'baekdugbn': 'tbmt', 'baekdugbnname': '태백산권',
         'baekdurealdistance': '11.3㎞', 'baekdusectione': '도래기재', 'baekdusections': '박달령', 'baekduspect': '구룡산',
         'baekduvia': '박달령→옥돌봉→도래기재', 'mntloca': '강원도 태백시, 경상북도 봉화군 석포면',
         'mntnfile': ' http://www.forest.go.kr/images/data/down/mount/2214211300.zip', 'mntnnm': '태백산'
        },
        {'baekduId': 'BAEK_32', 'baekdudistance': '14.4㎞', 'baekdugbn': 'tbmt', 'baekdugbnname': '태백산권',
         'baekdurealdistance': '26.5㎞', 'baekdusectione': '장바위', 'baekdusections': '도래기재', 'baekduspect': '구룡산',
         'baekduvia': '도래기재→구룡산→고치령→장바위', 'mntloca': '강원 도 태백시, 경상북도 봉화군 석포면',
         'mntnfile': ' http://www.forest.go.kr/images/data/down/mount/2214211300.zip', 'mntnnm': '태백산'
        },
        {'baekduId': 'BAEK_33', 'baekdudistance': '10.1㎞', 'baekdugbn': 'tbmt', 'baekdugbnname': '태백산권',
         'baekdurealdistance': '18.6㎞', 'baekdusectione': '화방재', 'baekdusections': '장바위', 'baekduspect': '태백산, 유일사',
         'baekduvia': '장바위→태백산→화방재', 'mntloca': '강원도  태백시, 경상북도 봉화군 석포면',
         'mntnfile': ' http://www.forest.go.kr/images/data/down/mount/2214211300.zip', 'mntnnm': '태백산'
        },
        {'baekduId': 'BAEK_34', 'baekdudistance': '14.5㎞', 'baekdugbn': 'tbmt', 'baekdugbnname': '태백산권',
         'baekdurealdistance': '26.8㎞', 'baekdusectione': '1233.1고지', 'baekdusections': '화방재', 'baekduspect': '함백산',
         'baekduvia': '화방재→함백산→싸리재→1233.1고지', 'mntloca': ' 강원도 태백시, 경상북도 봉화군 석포면',
         'mntnfile': ' http://www.forest.go.kr/images/data/down/mount/2214211300.zip', 'mntnnm': '태백산'
        },
    ]
    info = {
        "keys": ["baekduId", "baekdudistance", "baekdugbn", "baekdugbnname", "baekdurealdistance",
                 "baekdusectione", "baekdusections", "baekduspect", "baekduvia", "mntloca",
                 "mntnfile", "mntnnm"
        ],
        "file": "/home/sanxoo/extrad/file/20211125000000_ID.csv"
    }
    save(info, items)



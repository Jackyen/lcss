# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import sys
from datetime import timedelta, date, datetime

pick_dates = ['2019/7/29', '2019/7/30', '2019/7/31']
start_date = '2019/8/1'
end_date = '2019/8/31'
Cstart_date = '2019/7/29'
Cend_date = '2019/8/31'

day_range = [d.strftime('%Y/%-m/%-d').lstrip("0") for d in pd.date_range(start_date, end_date)]
dataset_range = [d.strftime('%Y/%-m/%-d').lstrip("0") for d in pd.date_range('2019/7/29', '2019/8/31')]

epsilon = 0.005


def read_dataset():
    df = pd.read_csv('origin1.csv', parse_dates=['date'])
    origin_df = pd.DataFrame(df).fillna(0)
    return df, origin_df

def lcss():
    cluster = {}
    # use to store text message
    cluster_str = {}

    start_cal = datetime.strptime(start_date, "%Y/%m/%d")
    end_cal = datetime.strptime(end_date, "%Y/%m/%d")

    df, origin_df = read_dataset()

    # 有遺失值的觀測值填補 0
    origin_df = origin_df.fillna(0)
    # print(filled_value)
    # export_csv(cluster, df)

    select_df = origin_df.loc[(df['date'] >= start_date) & (df['date'] <= end_date)]

    result = {}
    for d in pick_dates:
        pick_df = origin_df.loc[(df['date'] == d)]
        result[d] = compare_day(pick_df, select_df, df, 1)

        # init the cluster
        cluster[d] = [d]
        cluster_str[d] = [d]

    # r = pd.DataFrame(result, index=day_range)
    # 正規化，d_lcss
    for key, value in result.items():
        result[key] = list(map(lambda x: 1 - (x / 1440), value))

    # 從裡面選出 cluster 值
    for i in range(len(day_range)):
        k = 'date'
        v = 1
        s = ''
        for d in pick_dates:
            if result[d][i] <= v:
                k = d
                v = result[d][i]
                s = day_range[i]
        cluster[k].append(s)
        # add the str value to the cluster
        cluster_str[k].append(s + ' ' + str(v))

    print(cluster)

    r = pd.DataFrame(result, index=day_range)
    print(r)

    export_csv(cluster, df)


def export_csv(cluster, df):
    # cluster = {'2019/7/29': ['2019/7/29', '2019/8/2', '2019/8/3', '2019/8/5', '2019/8/6', '2019/8/7', '2019/8/12', '2019/8/13', '2019/8/14', '2019/8/15', '2019/8/16', '2019/8/19', '2019/8/21', '2019/8/23', '2019/8/24', '2019/8/26', '2019/8/27', '2019/8/28', '2019/8/29', '2019/8/30'], '2019/7/30': ['2019/7/30'], '2019/7/31': ['2019/7/31', '2019/8/1', '2019/8/4', '2019/8/8', '2019/8/9', '2019/8/10', '2019/8/11', '2019/8/17', '2019/8/18', '2019/8/20', '2019/8/22', '2019/8/25', '2019/8/31']}

    frame_list = []
    origin_df = pd.DataFrame(df).fillna(0)

    for k, v in cluster.items():

        sample = {'uid': [''] * 1440, 'date': [''] * 1440, 'hr': [''] * 1440, 'min': [''] * 1440,
                  'timestamp': [l for l in range(1440)], 'smo_x': [0] * 1440, 'smo_y': [0] * 1440}
        e_x = [0] * 1440
        e_y = [0] * 1440
        for d in v:
            pick_df = origin_df.loc[(df['date'] == d)]
            for i in range(1440):
                if pick_df.smo_x.size == 0:
                    break
                else:
                    if pick_df.smo_x.values[i] != 0:
                        e_x[i] += 1
                    if pick_df.smo_y.values[i] != 0:
                        e_y[i] += 1
                    sample['smo_x'][i] = sample['smo_x'][i] + pick_df.smo_x.values[i]
                    sample['smo_y'][i] = sample['smo_y'][i] + pick_df.smo_y.values[i]
        sample['smo_x'] = list(map(lambda x, y: x / y if y != 0 else 0, sample['smo_x'], e_x))
        sample['smo_y'] = list(map(lambda x, y: x / y if y != 0 else 0, sample['smo_y'], e_y))
        t = pd.DataFrame(sample)
        frame_list.append(t)

    for i, v in enumerate(frame_list):
        v.to_csv('out/' + str(i) + '.csv', index=False)


def compare_day(day_df, range_df, df, method):
    month_count = []
    # print(day_df[0:10])

    # pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])

    # com_df = range_df.loc[(df['date'] == '2019/8/17')]
    # print(com_df.date)
    if method == 2:
        day_range = [d.strftime('%Y/%-m/%-d').lstrip("0") for d in pd.date_range(Cstart_date, Cend_date)]
    else :
        day_range = [d.strftime('%Y/%-m/%-d').lstrip("0") for d in pd.date_range(start_date, end_date)]

    for d in day_range:
        s = 0
        total_count = 0
        com_df = range_df.loc[(df['date'] == d)]
        # com_df = range_df.loc[(df['date'] == '2019/8/17')]

        print(d)
        while s <= 1439:
            flag = 0
            for i in range(s, s + 11):
                n = i % 1440
                if (com_df.smo_x.size == 0) | (day_df.smo_x.size == 0):
                    break
                if (com_df.smo_x.values[n] == 0) | (day_df.smo_x.values[s] == 0):
                    continue
                if (abs(com_df.smo_x.values[n] - day_df.smo_x.values[s]) > epsilon) | (
                        abs(com_df.smo_y.values[n] - day_df.smo_y.values[s]) > epsilon):
                    flag = 0
                    break
                flag = 1
            # print(flag)
            total_count = total_count + flag
            s = s + 1
        month_count.append(total_count)
    return month_count


def lcss2(l):
    cluster = {}
    # use to store text message
    cluster_str = {}

    df, origin_df = read_dataset()

    pick_dates_df = []
    pick_dates = range(int(l))
    for i in pick_dates:
        df_temp = pd.read_csv('in/' + str(i) + '.csv', parse_dates=['date'])
        temp = pd.DataFrame(df_temp)
        pick_dates_df.append(temp)

    result = {}

    for d in pick_dates:
        result[d] = compare_day(pick_dates_df[d], origin_df, df, 2)

        # init the cluster
        cluster[d] = ['cluster'+str(d)]
        cluster_str[d] = ['cluster'+str(d)]

    # 正規化，d_lcss
    for key, value in result.items():
        result[key] = list(map(lambda x: 1 - (x / 1440), value))

    # 從裡面選出 cluster 值
    for i in range(len(dataset_range)):
        k = 'date'
        v = 1
        s = ''
        for d in pick_dates:
            if result[d][i] <= v:
                k = d
                v = result[d][i]
                s = dataset_range[i]
        cluster[k].append(s)
        # add the str value to the cluster
        cluster_str[k].append(s + ' ' + str(v))

    print(cluster)

    r = pd.DataFrame(result, index=dataset_range)
    print(r)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = sys.argv[1:]
    # # lcss2(3)
    # lcss()
    if args[0] == 'lcss':
        lcss()
    elif args[0] == 'lcss2':
        lcss2(args[1])

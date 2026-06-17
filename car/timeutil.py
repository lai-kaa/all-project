import datetime

# 时间比较：入场时间是否在有效期之后（业主卡过期判断，现在不用，保留兼容）
def time_cmp(validityDate, nowDate):
    try:
        v_time = datetime.datetime.strptime(validityDate, '%Y-%m-%d %H:%M')
        n_time = datetime.datetime.strptime(nowDate, '%Y-%m-%d %H:%M')
        return v_time > n_time
    except:
        return False

# 计算停车时长（小时）
def priceCalc(inTime, outTime):
    t1 = datetime.datetime.strptime(inTime, '%Y-%m-%d %H:%M')
    t2 = datetime.datetime.strptime(outTime, '%Y-%m-%d %H:%M')
    diff = t2 - t1
    hours = diff.total_seconds() / 3600
    return max(1, round(hours))
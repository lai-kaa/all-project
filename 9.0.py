import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker

# 导入所需的数据分析和可视化库
# numpy：用于数值计算，处理数组相关操作
# pandas：用于数据读取、清洗和基础统计分析
# matplotlib.pyplot：用于绘制各类图表，展示数据趋势和分布
# seaborn：基于matplotlib的可视化库，让图表更美观
# matplotlib.ticker：用于设置图表坐标轴刻度相关参数

# 设置绘图风格和中文字体，避免中文显示乱码
plt.style.use('ggplot')  # 设置绘图风格为ggplot，简洁美观
sns.set(style='darkgrid',font_scale=1.2)  # 设置seaborn风格为深色网格，字体放大1.2倍
plt.rcParams['font.family'] = 'SimHei'  # 设定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号显示异常的问题

# 读取s数据集，文件路径为当前目录下的douyin_dataset.csv
data = pd.read_csv('douyin_dataset.csv')
# 查看数据集前5行数据，快速了解数据的结构和内容
print(data.head())

# 查看数据集的所有列名，明确各字段的含义，为后续分析做准备
print(data.columns)

# 查看数据集的形状，输出格式为（行数，列数），了解数据量大小
print(data.shape)

# 查看数据集的详细信息，包括每列的数据类型、非空值数量
# show_counts=True表示显示每列的非空值和空值具体数量，便于判断缺失情况
print(data.info(show_counts=True))

# 查看数据集的基本统计描述，包括计数、均值、标准差、最小值、最大值和四分位数
# 仅对数值型字段有效，用于快速掌握数据的分布特征
print(data.describe())

# 统计每列的缺失值数量，判断数据缺失情况，为后续数据清洗提供依据
print(data.isnull().sum())

# 统计数据集中的重复数据数量，重复数据会影响分析结果，需后续处理或确认
print(data.duplicated().sum())

# 重命名指定列，将原列名Unnamed: 0改为ID，使列名更具可读性
colNameDict ={'Unnamed: 0':'ID'}
data.rename(columns=colNameDict,inplace=True)  # inplace=True表示直接修改原数据集，不创建新对象

# 转换时间格式，将real_time列从字符串类型转为datetime类型，便于后续时间相关分析
# format参数指定原时间字符串的格式，确保转换准确
data['real_time'] = pd.to_datetime(data['real_time'],format='%Y-%m-%d %H:%M:%S')
# 从real_time列中提取日期部分，生成新的date列，用于按日期分组统计
data['date'] = data['real_time'].dt.date

# 查看转换后的ID、real_time、date三列数据，确认时间转换和日期提取是否成功
print(data[['ID','real_time','date']].head())

# 按日期分组，统计每日的播放量（以ID列计数，每个ID代表一次播放）
data_id = data.groupby('date').count()['ID']
# 查看每日播放量的前5条数据，确认分组统计结果
print(data_id.head())

# 按日期分组，统计每日的独立用户数（uid为用户唯一标识，nunique()计算唯一值数量）
data_uid = data.groupby('date')['uid'].nunique()
# 查看每日独立用户数的前5条数据
print(data_uid.head())

# 按日期分组，统计每日的独立作者数（author_id为作者唯一标识）
data_author = data.groupby('date')['author_id'].nunique()
# 查看每日独立作者数的前5条数据
print(data_author.head())

# 按日期分组，统计每日的独立作品数（item_id为作品唯一标识）
data_item = data.groupby('date')['item_id'].nunique()
# 查看每日独立作品数的前5条数据
print(data_item.head())

# 绘制日播放量、日用户量、日作者量、日作品量随时间变化的趋势图
x = data_id.index  # x轴为日期，与各指标的分组索引一致
plt.figure(figsize=(12,12))  # 设置图表大小，宽12英寸，高12英寸
ax1 = plt.subplot(411)  # 划分4行1列的子图，当前绘制第1个子图
plt.plot(x.values,data_id.values)  # 绘制日播放量趋势线
plt.setp(ax1.get_xticklabels(),visible = False)  # 隐藏当前子图的x轴标签，避免与最后一个子图重复
plt.title('日播放量 日用户量 日作者量 日作品量随时间变化趋势')  # 设置总标题
plt.ylabel('日播放量')  # 设置当前子图的y轴标签

ax2 = plt.subplot(412,sharex=ax1)  # 绘制第2个子图，与第1个子图共享x轴
plt.plot(x.values,data_uid.values)  # 绘制日用户量趋势线
plt.setp(ax2.get_xticklabels(),visible = False)  # 隐藏x轴标签
plt.ylabel('日用户量')  # 设置y轴标签

ax3 = plt.subplot(413,sharex=ax1)  # 绘制第3个子图，共享x轴
plt.plot(x.values,data_author.values)  # 绘制日作者量趋势线
plt.setp(ax3.get_xticklabels(),visible = False)  # 隐藏x轴标签
plt.ylabel('日作者量')  # 设置y轴标签

ax4 = plt.subplot(414,sharex=ax1)  # 绘制第4个子图，共享x轴
plt.plot(x.values,data_item.values)  # 绘制日作品量趋势线
plt.ylabel('日作品量')  # 设置y轴标签
plt.show()  # 显示图表

# 筛选播放量前50的作者数据，用于分析头部作者的表现
# 先统计每个作者的作品数量（按author_id分组计数），取前50名的作者ID
author_top50_idx = data['author_id'].value_counts().iloc[:50].index
# 筛选出这50名作者的所有相关数据，形成新的数据集
author_50 = data[data['author_id'].isin(author_top50_idx)]
# 查看前50名作者数据集的前5行，确认筛选结果
print(author_50.head())

# 计算前50名作者的平均点赞率，按author_id分组，对like列取均值，再按前50名作者ID筛选
author_1_50=data.groupby('author_id')['like'].mean().loc[author_top50_idx]
# 查看前50名作者平均点赞率的前5条数据
author_1_50.head()

# 计算前50名作者的作品占比，即前50名作者的作品数量占总作品数量的比例
author_p_50=data['author_id'].value_counts().iloc[:50]/len(data['ID'])
# 查看前50名作者作品占比的前5条数据
author_p_50.head()

# 绘制前50名作者的作品数量与播放率、点赞率关系图
x=author_top50_idx.astype(str)  # 将作者ID转为字符串类型，便于x轴显示
y1=author_p_50.values  # y1轴为前50名作者的作品占比
y2=author_1_50.values  # y2轴为前50名作者的平均点赞率
fig,ax1=plt.subplots(figsize=(18,8))  # 设置图表大小，宽18英寸，高8英寸
color='tab:blue'  # 设置第一个y轴的颜色
ax1.bar(x, y1, color=color)  # 绘制作品占比的柱状图
ax1.set_xlabel('作者 ID')  # 设置x轴标签
ax1.set_ylabel('作品数量', color=color)  # 设置第一个y轴标签，颜色与柱状图一致
ax1.tick_params(axis='y', labelcolor=color)  # 设置第一个y轴刻度的颜色
plt.xticks(rotation=-45)  # 将x轴标签旋转45度，避免重叠
plt.title('作品数量与播放率、点赞率关系', fontsize=24)  # 设置图表标题，字体大小24

# 创建第二个y轴，与第一个y轴共享x轴，用于显示点赞率
ax2=ax1.twinx()
color='tab:red'  # 设置第二个y轴的颜色
ax2.set_ylabel('作品点赞率', color=color)  # 设置第二个y轴标签
ax2.tick_params(axis='y', labelcolor=color)  # 设置第二个y轴刻度的颜色

# 计算前50名作者的作品播放率，即每个作者的作品数量占总播放量的比例
author_play_rate = data.groupby('author_id').count()['ID'].loc[author_top50_idx] / len(data)
y3 = author_play_rate.values  # y3轴为前50名作者的作品播放率
# 创建第三个y轴，与第一个y轴共享x轴，用于显示播放率
ax3=ax1.twinx()
color='tab:pink'  # 设置第三个y轴的颜色
ax3.plot(x,y3,color=color)  # 绘制播放率的折线图
ax3.set_ylabel('作品播放率', color=color, fontsize=30)  # 设置第三个y轴标签，字体大小30
ax3.tick_params(axis='y', labelcolor=color)  # 设置第三个y轴刻度的颜色
plt.show()  # 显示图表

# 计算所有作者的作品播放量累计占比，用于分析头部作者的贡献度
# 先按作者作品数量降序排序，再计算累计和，最后除以总播放量得到累计占比
author_p=data['author_id'].value_counts().cumsum()/len(data['ID'])
# 查看累计占比的前5条数据
author_p.head()

# 绘制作者作品播放量贡献分布图（洛伦兹曲线），展示头部作者的贡献情况
x=np.array(range(len(author_p)))/len(author_p)  # x轴为作者数量占比（归一化处理）
plt.figure(figsize=(12,6))  # 设置图表大小
plt.plot(x,author_p.values)  # 绘制累计占比折线图
plt.title("平台作品播放量贡献")  # 设置图表标题
plt.xlabel("作者作品数量占比")  # 设置x轴标签
plt.ylabel("播放量占比")  # 设置y轴标签
plt.show()  # 显示图表

# 按作品时长分组，统计不同时长作品的播放量（以uid计数，代表播放次数）
duration_uids_nums=data.groupby('duration_time').count()['uid']
# 按作品时长升序排序，查看不同时长作品的数量分布
data['duration_time'].value_counts().sort_index(ascending=True)
# 查看不同时长作品播放量的前5条数据
duration_uids_nums.head()

# 按作品时长分组，统计不同时长作品的平均完播率和平均点赞率
duration_time_finish=data.groupby('duration_time')[['finish', 'like']].mean()
# 筛选出播放量大于100的作品时长数据，避免样本量过少导致的结果偏差
duration_time_f_1=duration_time_finish[duration_uids_nums>100]
# 查看筛选后的数据前5条
duration_time_f_1.head()

# 按作品时长分组，统计不同时长的独立作品数量
duration_item_nums=data.groupby('duration_time')['item_id'].nunique()
# 查看不同时长独立作品数量的前5条数据
duration_item_nums.head()

# 绘制作品时长与播放量、作品数量、完播率、点赞率的关系图（2行2列子图）
fig=plt.figure(figsize=(20,16))  # 设置图表总大小
fig.subplots_adjust(hspace=0.2)  # 调整子图之间的垂直间距
ax1=fig.add_subplot(2,2,1)  # 划分2行2列子图，当前绘制第1个子图（左上）
duration_uids_nums.plot(ax=ax1)  # 绘制作品时长与播放量的关系线
plt.xlim(2,40)  # 设置x轴范围为2到40，聚焦主要时长区间
plt.xlabel('作品时长')  # 设置x轴标签
plt.ylabel('播放量')  # 设置y轴标签
plt.title("作品时长与播放量的关系")  # 设置子图标题
plt.grid(True)  # 显示网格线，便于读取数据

ax2=fig.add_subplot(2,2,2)  # 绘制第2个子图（右上）
duration_item_nums.plot(ax=ax2)  # 绘制作品时长与作品数量的关系线
plt.xlim(2,40)  # 设置x轴范围
plt.xlabel('作品时长')  # 设置x轴标签
plt.ylabel('作品数量')  # 设置y轴标签
plt.title("作品时长与作品数量的关系")  # 设置子图标题
plt.grid(True)  # 显示网格线

ax3=fig.add_subplot(2,2,3)  # 绘制第3个子图（左下）
duration_time_f_1.plot(ax=ax3,y='finish')  # 绘制作品时长与完播率的关系线
plt.xlim(2,40)  # 设置x轴范围
plt.xlabel('作品时长')  # 设置x轴标签
plt.ylabel('完播率')  # 设置y轴标签
plt.title("作品时长与完播率的关系")  # 设置子图标题
plt.grid(True)  # 显示网格线

ax4=fig.add_subplot(2,2,4)  # 绘制第4个子图（右下）
duration_time_f_1.plot(ax=ax4,y='like')  # 绘制作品时长与点赞率的关系线
plt.xlim(2,40)  # 设置x轴范围
plt.xlabel('作品时长')  # 设置x轴标签
plt.ylabel('点赞率')  # 设置y轴标签
plt.title("作品时长与点赞率的关系")  # 设置子图标题
plt.grid(True)  # 显示网格线
plt.show()  # 显示图表

# 按作品发布小时（H列）分组，统计不同发布小时的平均完播率和平均点赞率
H_f_1=data.groupby('H')[['finish', 'like']].mean()
# 查看不同发布小时的完播率和点赞率前5条数据
H_f_1.head()

# 绘制作品发布时间（小时）与点赞率、完播率的关系图
plt.figure(figsize=(12,8))  # 设置图表大小
H_f_1.plot()  # 绘制两条折线，分别代表完播率和点赞率
plt.xlabel('作品发布时间', fontsize=10)  # 设置x轴标签，字体大小10
plt.ylabel('点赞率和完播率', fontsize=10)  # 设置y轴标签，字体大小10
plt.title("作品发布时间与点赞率、完播率之间的关系", fontsize=10)  # 设置图表标题，字体大小10
plt.show()  # 显示图表

# 按作品发布小时分组，统计不同发布小时的播放量
H_uid=data.groupby('H').count()['uid']
# 查看不同发布小时播放量的前5条数据
H_uid.head()

# 计算24小时内的平均播放量，用于绘制参考线
H_u_m=H_uid.mean()

# 按作品发布小时分组，统计不同发布小时的投稿数（独立作品数量）
H_item=data.groupby('H')['item_id'].nunique()
# 查看不同发布小时投稿数的前5条数据
H_item.head()

# 绘制24小时内播放量与投稿数的变化关系图，共享x轴
fig=plt.figure()  # 创建图表对象
ax1=fig.add_subplot(111)  # 绘制单个子图
ax1.plot(H_uid,c='#87CEFA', label='播放量')  # 绘制播放量折线图，颜色为浅蓝色
plt.legend(loc='upper left')  # 设置播放量图例位置在左上角
plt.axhline(y=H_u_m, ls='--', c='b')  # 绘制平均播放量参考线，虚线，蓝色
plt.xlabel('作品发布时间')  # 设置x轴标签
plt.ylabel('播放量')  # 设置第一个y轴标签

ax2=ax1.twinx()  # 创建第二个y轴，共享x轴
ax2.plot(H_item, label='投稿数')  # 绘制投稿数折线图
plt.legend(loc='upper right')  # 设置投稿数图例位置在右上角
plt.ylabel('投稿数')  # 设置第二个y轴标签
plt.title("24小时内播放量与投稿数的变化")  # 设置图表标题
plt.show()  # 显示图表

# 按背景音乐（music_id）分组，统计播放量前20的背景音乐
music_20=data['music_id'].value_counts().iloc[:20]
# 查看播放量前20背景音乐的前5条数据
music_20.head()

# 计算所有背景音乐的播放量累计占比，分析热门背景音乐的贡献度
music_p=data['music_id'].value_counts().cumsum()/len(data['ID'])
# 查看背景音乐播放量累计占比的前5条数据
music_p.head()

# 统计播放量前20背景音乐的平均完播率和平均点赞率
# 先按music_id分组计算均值，再按前20名背景音乐ID筛选
music_f1=data.groupby('music_id')[['finish', 'like']].mean().loc[music_20.index.values]
# 查看前20背景音乐的完播率和点赞率前5条数据
music_f1.head()

# 计算每个背景音乐的播放量占总用户数的比例（辅助分析）
data['music_id'].value_counts()/len(data['uid'])

# 绘制播放量前20背景音乐与播放量的关系柱状图
x=music_20.index.astype('str').values  # 将音乐ID转为字符串，便于x轴显示
y=music_20.values  # y轴为背景音乐的播放量
plt.figure(figsize=(12,4))  # 设置图表大小
plt.bar(x,y)  # 绘制柱状图
plt.xlabel('歌曲 ID')  # 设置x轴标签
plt.ylabel('播放量')  # 设置y轴标签
plt.title('top20 背景音乐与播放量关系')  # 设置图表标题
plt.show()  # 显示图表

# 绘制背景音乐播放量累计占比贡献图（洛伦兹曲线）
x=np.array(range(len(music_p)))/len(music_p)  # x轴为背景音乐数量占比（归一化）
y=music_p.values  # y轴为播放量累计占比
plt.figure(figsize=(12,4))  # 设置图表大小
plt.plot(x,y)  # 绘制累计占比折线图
plt.title("音乐播放量累计占比贡献")  # 设置图表标题
plt.xlabel("音乐数量占比")  # 设置x轴标签
plt.ylabel("音乐播放量占比")  # 设置y轴标签
plt.show()  # 显示图表

# 绘制播放量前20背景音乐的完播率和点赞率对比图（2行1列子图）
x=music_f1.finish.index.astype('str').values  # x轴为音乐ID，转为字符串
y=music_f1.finish.values  # y轴为完播率
fig2,music_axes=plt.subplots(2,1,figsize=(16,12),sharex=True)  # 设置图表大小，共享x轴
plt.subplot(211)  # 绘制第1个子图（上）
plt.plot(x,y)  # 绘制完播率折线图
plt.title("排名前20的热门音乐完播率")  # 设置子图标题
music_axes[0].set_ylabel("完播率")  # 设置第1个子图的y轴标签
music_axes[0].set_xlabel("音乐 id")  # 设置x轴标签
# 绘制完播率平均值参考线，虚线，橙色
plt.axhline(y=music_f1.finish.mean(),ls='--',color='orange')

plt.subplot(212)  # 绘制第2个子图（下）
x=music_f1.like.index.astype('str').values  # x轴为音乐ID，转为字符串
y=music_f1.like.values  # y轴为点赞率
plt.plot(x,y)  # 绘制点赞率折线图
plt.title("排名前20的热门音乐点赞率")  # 设置子图标题
music_axes[1].set_ylabel("点赞率")  # 设置第2个子图的y轴标签
music_axes[1].set_xlabel("音乐 id")  # 设置x轴标签
# 绘制点赞率平均值参考线，虚线，橙色
plt.axhline(y=music_f1.like.mean(),ls='--',color='orange')
plt.tight_layout()  # 自动调整子图间距，避免标签重叠
plt.show()  # 显示图表

# 按背景音乐和日期分组，统计每个背景音乐每日的播放量
m_d_d=data.groupby(['music_id', 'date'])['uid'].count()
# 筛选播放量前10的背景音乐ID，用于分析热门音乐的日播放量变化
top10_music = data.groupby('music_id')['uid'].count().sort_values(ascending=False).iloc[:10].index.tolist()
# 筛选出前10背景音乐的每日播放量数据
m_d_d = m_d_d.loc[top10_music]
# 查看前10背景音乐每日播放量的前5条数据
m_d_d.head()

# 将分组数据转换为宽格式，便于绘制趋势图（行为日期，列为音乐ID）
m_d_d.unstack().T.head()

# 绘制前10背景音乐的日播放量变化趋势图
m_d_d.unstack().T.plot()  # 每一条线代表一个背景音乐的日播放量变化
plt.title("top10 音乐播放量日变化")  # 设置图表标题
plt.legend(loc='best')  # 自动选择最佳图例位置
plt.show()  # 显示图表

# 按日期分组，统计全平台核心运营指标，用于监控平台整体表现
# 日播放量：每日总播放次数（以uid计数）
d_uid=data.groupby('date').count()['uid']
# 日用户：每日独立用户数（uid唯一值数量）
d_uid_n=data.groupby('date')['uid'].nunique()
# 日制作者：每日独立作者数（author_id唯一值数量）
d_auth=data.groupby('date')['author_id'].nunique()
# 日投稿数：每日独立作品数（item_id唯一值数量）
d_item=data.groupby('date')['item_id'].nunique()

# 绘制全平台每日核心指标变化图（2行2列子图）
plt.figure(figsize=(16,12))  # 设置图表总大小
plt.subplot(221)  # 绘制第1个子图（左上）
d_uid.plot()  # 绘制每日总播放量趋势线
plt.title("全平台每日总播放量变化")  # 设置子图标题

plt.subplot(222)  # 绘制第2个子图（右上）
d_uid_n.plot()  # 绘制每日独立用户数趋势线
plt.title("全平台每日用户数变化")  # 设置子图标题

plt.subplot(223)  # 绘制第3个子图（左下）
d_auth.plot()  # 绘制每日独立作者数趋势线
plt.title("全平台每日制作者变化")  # 设置子图标题

plt.subplot(224)  # 绘制第4个子图（右下）
d_item.plot()  # 绘制每日独立作品数趋势线
plt.title("全平台每日投稿作品数变化")  # 设置子图标题
plt.show()  # 显示图表

# 按作品来源渠道（channel）分组，统计各渠道的播放量
channel=data.groupby('channel').count()['uid']
labels=channel.index  # 获取渠道ID，作为饼图的标签

# 为渠道ID添加对应说明，便于图表解读
labels2=labels.map({0:'0:手机软件', 2:'2:浏览器', 3:'3:微信分享', 4:'4:用户搜索'})
plt.figure(figsize=(8, 6))  # 设置图表大小
plt.axes(aspect=1)  # 设置坐标轴比例为1:1，使饼图为正圆形
# 绘制饼图，显示各渠道占比，保留2位小数，设置标签和百分比位置
plt.pie(channel, labels=labels, autopct='%0.2f%%', labeldistance=0.8, pctdistance=1.2)
plt.title("某视频平台作品来源分布扇形图")  # 设置图表标题
plt.legend(labels=labels2, loc='upper right')  # 设置图例，显示渠道说明，位置在右上角
plt.show()  # 显示图表

# 分析活动期间（2019-10-21至2019-10-30）的新增用户情况
# 筛选活动期间的用户数据（newusers）
newusers=data[(data['date'].astype(str)>='2019-10-21') & (data['date'].astype(str)<'2019-10-30')]['uid']
# 筛选活动前的用户数据（oldusers）
oldusers=data[data['date'].astype(str)<'2019-10-21']['uid']
# 计算活动期间新增用户数：活动期间独立用户数 - 活动期间的老用户数（在活动前已存在的用户）
addedusers=newusers.nunique()-newusers[newusers.isin(oldusers)].nunique()
# 打印活动期间新增用户总数
print('活动期间新增总人数:{}'.format(addedusers))

# 统计活动期间的总播放次数（以newusers计数）
newusers.count()

# 分析活动前后的播放量变化
# 计算活动前（2019-09-21至2019-10-20）的平均日播放量
pv_before=data.groupby("date")["uid"].count()[lambda x: (x.index.astype(str)>='2019-09-21') & (x.index.astype(str)<='2019-10-20')].mean()
# 计算活动期间（2019-10-21至2019-10-30）的平均日播放量
pv_after=data.groupby("date")["uid"].count()[lambda x: (x.index.astype(str)>='2019-10-21') & (x.index.astype(str)<='2019-10-30')].mean()
# 计算活动后与活动前平均日播放量的倍数关系
pv_n=pv_after/pv_before
# 打印播放量倍数关系，保留2位小数
print("活动后播放量是活动前的%.2f倍"%pv_n)

# 分析活动前后的日活跃用户数（DAU）变化
# 计算活动前的平均日活跃用户数
dau_before=data.groupby("date")["uid"].nunique()[lambda x: (x.index.astype(str)>='2019-09-21') & (x.index.astype(str)<='2019-10-20')].mean()
# 计算活动期间的平均日活跃用户数
dau_after=data.groupby("date")["uid"].nunique()[lambda x: (x.index.astype(str)>='2019-10-21') & (x.index.astype(str)<='2019-10-30')].mean()
# 计算活动后与活动前平均日活跃用户数的倍数关系
dau_n=dau_after/dau_before
# 打印日活跃用户数倍数关系，保留2位小数
print("活动后的日活跃用户数是活动前的%.2f倍"%dau_n)

# 绘制活动前后关键指标对比柱状图（1行3列子图）
fig=plt.figure(figsize=(16,12))  # 设置图表总大小
plt.subplot(131)  # 绘制第1个子图（左）：活动前后人数对比
X=['newusers', 'oldusers']  # x轴标签：活动期间用户、活动前用户
Y=[newusers.count(), oldusers.count()]  # y轴数据：活动期间总播放次数、活动前总播放次数
plt.bar(X,Y,width=0.5)  # 绘制柱状图，宽度0.5
plt.title('活动前后人数对比')  # 设置子图标题
plt.xlabel('用户')  # 设置x轴标签
plt.ylabel('数量')  # 设置y轴标签

plt.subplot(132)  # 绘制第2个子图（中）：活动前后播放量对比
X=['pv_before', 'pv_after']  # x轴标签：活动前平均日播放量、活动后平均日播放量
Y=[pv_before, pv_after]  # y轴数据：对应平均日播放量
plt.bar(X,Y,width=0.5)  # 绘制柱状图
plt.title('活动前后播放量对比')  # 设置子图标题
plt.xlabel('播放量')  # 设置x轴标签
plt.ylabel('数量')  # 设置y轴标签

plt.subplot(133)  # 绘制第3个子图（右）：活动前后日活跃用户数对比
X=['dau_before', 'dau_after']  # x轴标签：活动前平均日活、活动后平均日活
Y=[dau_before, dau_after]  # y轴数据：对应平均日活
plt.bar(X,Y,width=0.5)  # 绘制柱状图
plt.title('活动前后用户数对比')  # 设置子图标题
plt.xlabel('用户数')  # 设置x轴标签
plt.ylabel('数量')  # 设置y轴标签
plt.show()  # 显示图表
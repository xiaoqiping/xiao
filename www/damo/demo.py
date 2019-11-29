import pyecharts.options as opts
from pyecharts.charts.basic_charts import bar

attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
v1 = [5, 20, 36, 10, 75, 90]
v2 = [10, 25, 8, 60, 20, 80]

bar = (
    bar.Bar()
        .add_xaxis(attr)
        .add_yaxis("商家A", v1, stack="stack1")
        .add_yaxis("商家B", v2, stack="stack1")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="柱状图数据堆叠示例"))
)

bar.render("bar_stack.html")


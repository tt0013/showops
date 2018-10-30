#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi


import datetime
from pyecharts import Line, Page
from pyecharts_snapshot.main import make_a_snapshot



def test():
    ti = str(datetime.date.today())

    page = Page()
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [5, 20, 360, 10, 10, 100]
    v2= [11, 23, 132, 30, 50, 97]
    line1 = Line("疯播流量统计图-1",ti,width=700, height=400)
    line1.add(
        "域名峰值(Mbps)",
        attr,
        v1,
        is_stack=True,
        mark_point=['max'],
        area_color="#00ff7f",
        is_symbol_show=True,
        is_fill=True,
        line_opacity=0.2,
        area_opacity=0.4,
    )
    page.add(line1)

    # line2 = Line("疯播流量统计图-2",ti,width=700, height=400)
    # line2.add(
    #     "域名峰值(Mbps)",
    #     attr,
    #     v2,
    #     is_stack=True,
    #     mark_point=['max'],
    #     # mark_point=['average'],
    #     area_color="#00ff7f",
    #     is_symbol_show=True,
    #     is_fill=True,
    #     line_opacity=0.2,
    #     area_opacity=0.4,
    #     # symbol=None,
    # )
    # page.add(line2)
    # page.render()

if __name__ == '__main__':
    test()
    make_a_snapshot(r'E:\Django_Node\showops\updatetask\echarts\render.html',r'E:\Django_Node\showops\updatetask\echarts\render.png')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file   :influxdlog.py
# @time   :2020/4/14 9:41
# @Author :jmgen
# @Version:1.0
# @Desc   :
from influxdb import InfluxDBClient

class Influxdblog:
    client = InfluxDBClient('127.0.0.1', 8086, timeout=10)
    def write_influxd(self, msg):
        json_body = [
            {
                "measurement": "logger",
                "tags": {
                    "loginfo": "loginfo"
                },
                "fields": {
                    "value": msg
                }
            }]
        self.client.switch_database('casemanage')
        self.client.write_points(json_body)

    def get_info(self):
        self.client.switch_database('casemanage')
        log=self.client.query('select value from logger;')
        print(log)

if __name__ == "__main__":
    log=Influxdblog()
    log.get_info()
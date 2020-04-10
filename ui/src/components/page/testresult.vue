<template>
    <div>
        <el-form :inline="true" class="demo-form-inline">
            <el-form-item label="项目名称">
                <el-select v-model="project" placeholder="请选择">
                    <el-option label="请选择" value=""></el-option>
                    <template v-for="item in projects">
                        <el-option :label="item[0]" :value="item">
                        </el-option>
                    </template>
                </el-select>
            </el-form-item>
            <el-form-item label="用例版本">
                <el-select v-model="caseversion" placeholder="请选择">
                    <el-option label="请选择" value=""></el-option>
                    <template v-for="item in caseversionview">
                        <el-option :label="item[0]" :value="item">
                        </el-option>
                    </template>
                </el-select>
            </el-form-item>
            <el-form-item label="测试计划">
                <el-select v-model="testplan" placeholder="请选择">
                    <el-option label="请选择" value=""></el-option>
                    <template v-for="item in testplanview">
                        <el-option :label="item" :value="item">
                        </el-option>
                    </template>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="statistics">结果统计</el-button>
            </el-form-item>
        </el-form>
        <p>按版本统计：</p>
        <div>
            <vxe-table
                    border
                    resizable
                    style="width: 100%"
                    show-overflow
                    ref="xTable"
                    :cell-style="versioncellstyle"
                    :data="versiontableData">
                <vxe-table-column field="序号" title="序号" type="seq" width="30"></vxe-table-column>
                <vxe-table-column
                        field="name"
                        title="测试结果统计"
                        width="240">
                </vxe-table-column>
                <vxe-table-column
                        field="resultpass"
                        title="Pass"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="resultfail"
                        title="Fail"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="resultblock"
                        title="Block"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="resultnotest"
                        title="NT"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="runcase"
                        title="执行用例数"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="totalcase"
                        title="总用例数">
                </vxe-table-column>
            </vxe-table>
        </div>
        <br>
        <div>
            <p>按模块统计：</p>
            <vxe-table
                    border
                    resizable
                    style="width: 100%"
                    show-overflow
                    ref="xTable"
                    :cell-style="modelcellstyle"
                    :data="modeltableData">
                <vxe-table-column field="序号" title="序号" type="seq" width="30"></vxe-table-column>
                <vxe-table-column
                        field="project"
                        title="项目"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="caseversion"
                        title="测试用例版本"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="testplan"
                        title="测试计划"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="model"
                        title="模块名称"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="tester"
                        title="测试执行人"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="resultpass"
                        title="Pass"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="resultfail"
                        title="Fail"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="resultblock"
                        title="Block"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="resultnotest"
                        title="NT"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="runcase"
                        title="执行用例数"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        field="totalcase"
                        title="总用例数">
                </vxe-table-column>
            </vxe-table>
        </div>
        <br>
        <div id="versionchart" style="width:1000px;height:400px;"></div>
        <div id="modelchart" style="width:1600px;height:400px;">
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "testresult",
        data() {
            return {
                url: process.env.VUE_APP_URL,
                projects: [],
                caseversions: [],
                testplans: [],
                caseversionview: [],
                testplanview: [],
                versiontableData: [],
                modeltableData: [],
                project: '',
                caseversion: '',
                testplan: '',
                versionoptions: {},
                options: {},
                modeldata: [],
                passdata: [],
                faildata: [],
                blockdata: [],
                notestdata: [],
                modelruncase: [],
                modeltotalcase: [],
            }
        },
        created() {
            this.getdata();
        },
        watch: {
            project: function (val) {
                let that = this;
                that.caseversionview = [];
                that.caseversion = '';
                that.j = 0;
                for (let i = 0; i < that.caseversions.length; i++) {
                    if (that.caseversions[i][1] === val[1]) {
                        that.caseversionview[that.j] = that.caseversions[i];
                        that.j++;
                    }
                }
                return that.caseversionview
            },
            caseversion: function (val) {
                let that = this;
                that.testplanview = [];
                that.testplan = '';
                that.j = 0;
                for (let i = 0; i < that.testplans.length; i++) {
                    if (that.testplans[i][1] === val[1] && that.testplans[i][2] === val[2]) {
                        that.testplanview[that.j] = that.testplans[i][0];
                        that.j++;
                    }
                }
                return that.testplanview
            },
        },
        methods: {
            statistics() {
                let that = this;
                that.project = this.project;
                that.caseversion = this.caseversion;
                that.testplan = this.testplan;
                const path = this.url + "/result/testresult";
                if (that.project !== "" && that.testplan !== "") {
                    axios
                        .post(path, {
                            project: that.project,
                            caseversion: that.caseversion,
                            testplan: that.testplan,
                        })
                        .then(function (response) {
                            if (parseInt(response.data.code) === 200) {
                                that.versiontableData = response.data.versiontableData;
                                that.modeltableData = response.data.modeltableData;
                                that.versionoptions = response.data.versionoptions;
                                that.options = response.data.options;
                                that.drawversionbar();
                                that.drawmodelbar();
                            }
                        })
                        .catch(function (error) {
                            console.log(error)
                        })
                } else {
                    this.$message.warning("请选择项目和测试计划")
                }
            },
            //获取数据库中已有的项目、测试计划
            getdata() {
                let that = this;
                const path = this.url + "/result/getdata";
                axios
                    .get(path)
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.projects = response.data.projects;
                            that.caseversions = response.data.caseversions;
                            that.testplans = response.data.testplans;
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            drawversionbar() {
                let that = this;
                let chart = that.echarts.init(document.getElementById('versionchart'));
                chart.setOption({
                        title: {text: that.testplan + '_测试结果统计'},
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'shadow'
                            }
                        },
                        xAxis: [
                            {
                                type: 'category',
                                axisTick: {show: false},
                                data: ['Pass', 'Fail', 'Block', 'NT', '执行数', '总数'],
                            }
                        ],
                        yAxis: {
                            type: 'value'
                        },
                        series: [
                            {
                                type: 'bar',
                                label: {
                                    show: true,
                                    formatter: '{c}',
                                    fontSize: 16,
                                },
                                data: that.versionoptions,
                                itemStyle: {
                                    normal: {
                                        color: function (params) {
                                            let colorList = ['#00FF00', '#FF0000', '#FFFF00', '#BEBEBE', '#4cabce', '#006699'];
                                            return colorList[params.dataIndex]
                                        }
                                    }
                                },
                            }
                        ]
                    }
                )
            },
            drawmodelbar() {
                let that = this;
                let chart = that.echarts.init(document.getElementById('modelchart'));
                that.model = that.options.model;
                that.passdata = that.options.passdata;
                that.faildata = that.options.faildata;
                that.blockdata = that.options.blockdata;
                that.notestdata = that.options.notestdata;
                that.modelruncase = that.options.modelruncase;
                that.modeltotalcase = that.options.modeltotalcase;
                chart.setOption({
                    color: ['#00FF00', '#FF0000', '#FFFF00', '#BEBEBE', '#4cabce', '#006699'],
                    title: {text: that.testplan + '_测试结果统计'},
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        data: ['Pass', 'Fail', 'Block', 'NT', '执行数', '总数']
                    },
                    xAxis: [
                        {
                            type: 'category',
                            axisTick: {show: false},
                            data: that.model,
                            axisLabel: {
                                interval: 0,
                                rotate: -30,
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value'
                        }
                    ],
                    series: [
                        {
                            name: 'Pass',
                            type: 'bar',
                            label: {
                                show: true,
                                formatter: '{c}',
                                fontSize: 16,
                            },
                            data: that.passdata
                        },
                        {
                            name: 'Fail',
                            type: 'bar',
                            label: {
                                show: true,
                                formatter: '{c}',
                                fontSize: 16,
                            },
                            data: that.faildata
                        },
                        {
                            name: 'Block',
                            type: 'bar',
                            label: {
                                show: true,
                                formatter: '{c}',
                                fontSize: 16,
                            },
                            data: that.blockdata
                        },
                        {
                            name: 'NT',
                            type: 'bar',
                            label: {
                                show: true,
                                formatter: '{c}',
                                fontSize: 16,
                            },
                            data: that.notestdata
                        },
                        {
                            name: '执行数',
                            type: 'bar',
                            label: {
                                show: true,
                                formatter: '{c}',
                                fontSize: 16,
                            },
                            data: that.modelruncase
                        },
                        {
                            name: '总数',
                            type: 'bar',
                            label: {
                                show: true,
                                formatter: '{c}',
                                fontSize: 16,
                            },
                            data: that.modeltotalcase
                        }
                    ]
                })
            },
            versioncellstyle({row, rowIndex, column, columnIndex}) {
                if (column.property === 'runcase') {
                    if (row.runcase !== row.totalcase) {
                        return {
                            backgroundColor: '#FFFF00'
                        }
                    } else if (row.runcase === row.totalcase) {
                        return {
                            backgroundColor: '#00FF00'
                        }
                    }
                }
            },
            modelcellstyle({row, rowIndex, column, columnIndex}) {
                if (column.property === 'runcase') {
                    if (row.runcase !== row.totalcase) {
                        return {
                            backgroundColor: '#FFFF00'
                        }
                    } else if (row.runcase === row.totalcase) {
                        return {
                            backgroundColor: '#00FF00'
                        }
                    }
                }
            }
        },
    }
</script>

<style scoped>

</style>

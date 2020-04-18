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
                    <div v-if='isshownewplan'>
                        <el-option label="" value="">
                            <p @click="newplan">新建测试计划</p></el-option>
                    </div>
                    <el-option label="请选择" value=""></el-option>
                    <template v-for="item in testplanview">
                        <el-option :label="item[0]" :value="item[0]">
                        </el-option>
                    </template>
                </el-select>
                <template v-if='isshow'>
                    <el-input style="width: 60%" v-model="plan" placeholder="输入测试计划名称" clearable></el-input>
                    <el-button type="primary" @click="save">保存</el-button>
                </template>
            </el-form-item>
            <el-form-item label="用例模块">
                <el-select v-model="model" placeholder="请选择">
                    <el-option label="请选择" value=""></el-option>
                    <template v-for="item in modelview">
                        <el-option :label="item" :value="item">
                        </el-option>
                    </template>
                </el-select>
            </el-form-item>
            <el-form-item label="关键字查询">
                <el-input placeholder="请输入关键字查询" v-model="key" clearable></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">查询</el-button>
            </el-form-item>
        </el-form>
        <vxe-table
                border
                resizable
                style="width: 100%"
                show-overflow
                ref="xTable"
                :cell-style="cellStyle"
                :data="tableData"
                @edit-closed="autosave"
                :edit-config="{trigger: 'click', mode: 'cell'}">
            <vxe-table-column field="ID" title="序号" type="seq" width="30"></vxe-table-column>
            <vxe-table-column
                    sortable
                    field="caseid"
                    title="用例编号"
                    width="80">
            </vxe-table-column>
            <vxe-table-column
                    sortable
                    field="model"
                    title="主模块"
                    width="80">
            </vxe-table-column>
            <vxe-table-column
                    field="submodel"
                    title="子模块"
                    width="60">
            </vxe-table-column>
            <vxe-table-column
                    sortable
                    field="level"
                    title="级别"
                    width="30">
            </vxe-table-column>
            <vxe-table-column
                    field="preconditions"
                    title="前提条件"
                    width="80">
            </vxe-table-column>
            <vxe-table-column
                    field="title"
                    title="标题"
                    width="100">
            </vxe-table-column>
            <vxe-table-column
                    field="step"
                    title="步骤"
                    width="160">
            </vxe-table-column>
            <vxe-table-column
                    field="expectresult"
                    title="期待结果"
                    width="120">
            </vxe-table-column>
            <vxe-table-column
                    field="remark"
                    title="备注">
            </vxe-table-column>
            <vxe-table-column
                    sortable
                    field="caseresult"
                    title="测试结果">
            </vxe-table-column>
            <vxe-table-column
                    field="bugid"
                    :edit-render="{name: 'input'}"
                    title="缺陷ID">
            </vxe-table-column>
            <vxe-table-column
                    field="bugtitle"
                    :edit-render="{name: 'input'}"
                    title="缺陷标题">
            </vxe-table-column>
            <vxe-table-column
                    field="bugremark"
                    :edit-render="{name: 'input'}"
                    title="缺陷备注">
            </vxe-table-column>
            <vxe-table-column
                    field="tester"
                    title="提交人">
            </vxe-table-column>
            <vxe-table-column
                    field="testtime"
                    title="提交时间">
            </vxe-table-column>
            <vxe-table-column
                    fixed="right"
                    field="operation"
                    title="操作"
                    width="320">
                <template v-slot="{ row }">
                    <vxe-button style="background: #00FF00" name="Pass" @click="test(row,$event)">Pass</vxe-button>
                    <vxe-button style="background: #FF0000" name="Fail" @click="test(row,$event)">Fail</vxe-button>
                    <vxe-button style="background: #FFFF00" name="Block" @click="test(row,$event)">Blocked</vxe-button>
                    <vxe-button style="background: #BEBEBE" name="NT" @click="test(row,$event)">NT</vxe-button>
                </template>
            </vxe-table-column>
        </vxe-table>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "executecase",
        data() {
            return {
                url: process.env.VUE_APP_URL,
                project: '',
                caseversion: '',
                testplan: '',
                model: '',
                key: '',
                tableData: [],
                testdata: [],
                caseversionview: [],
                testplanview: [],
                modelview: [],

                projects: [],
                caseversions: [],
                testplans: [],
                models: [],

                plan: '',
                inputnewplan: '',
                isshow: false,
                isshownewplan: false,
            }
        },
        created() {
            this.datainfo();
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
                        that.testplanview[that.j] = that.testplans[i];
                        that.j++;
                    }
                }
                if (that.project.length !== 0 && that.caseversion.length !== 0) {
                    that.isshownewplan = true;
                }
                return [that.testplanview, that.isshownewplan]
            },
            testplan: function (val) {
                let that = this;
                that.modelview = [];
                that.model = '';
                that.j = 0;
                if (val.length !== 0) {
                    that.isshow = false;
                    for (let i = 0; i < that.models.length; i++) {
                        if (that.models[i][1] === that.caseversion[1] && that.models[i][2] === that.caseversion[2]) {
                            that.modelview[that.j] = that.models[i][0];
                            that.j++;
                        }
                    }
                }
                return that.modelview
            },
        },

        methods: {
            newplan() {
                this.isshow = true;
            },
            save() {
                let that = this;
                that.project = this.project;
                that.caseversion = this.caseversion;
                that.plan = this.plan;
                const path = this.url + "/case/createplan";
                that.isshow = false;
                if (that.plan !== '') {
                    axios
                        .post(path, {
                            project: that.project,
                            caseversion: that.caseversion,
                            plan: that.plan,
                        })
                        .then(function (response) {
                            if (parseInt(response.data.code) === 200) {
                                console.log(response.data);
                                that.testplan = that.plan;
                                that.$message.success(response.data.msg);
                            }
                            else if (parseInt(response.data.code) === 40001) {
                                that.$message.warning(response.data.msg);
                            }
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
                }
                else {
                    that.$message.warning('测试计划名称不能为空');
                }
            },
            onSubmit() {
                let that = this;
                that.project = this.project;
                that.caseversion = this.caseversion;
                that.testplan = this.testplan;
                that.model = this.model;
                that.key = this.key;
                const path = this.url + "/case/excutecase";
                axios
                    .post(path, {
                        project: that.project,
                        caseversion: that.caseversion,
                        testplan: that.testplan,
                        model: that.model,
                        key: that.key,
                    })
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.tableData = response.data.tableData;
                        }
                        else if (parseInt(response.data.code) === 40001) {
                            that.$message.warning(response.data.msg)
                        }

                    })
                    .catch(function (error) {
                        console.log(error)
                    });
            },
            //获取数据库中已有的项目、用例版本、测试计划、功能模块数据
            datainfo() {
                let that = this;
                const path = this.url + "/case/datainfo";
                axios
                    .get(path)
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.projects = response.data.projects;
                            that.caseversions = response.data.caseversions;
                            that.testplans = response.data.testplans;
                            that.models = response.data.models
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            test(row, event) {
                let that = this;
                const path = this.url + "/case/upresult";
                that.project = this.project;
                that.caseversion = this.caseversion;
                that.testplan = this.testplan;
                that.model = this.model;
                that.key = this.key;
                that.casemodel = row.model;
                that.caseid = row.id;
                that.result = window.event.currentTarget.name;
                that.tester = localStorage.getItem('username');
                that.testtime = this.gettime();
                axios
                    .post(path, {
                        project: that.project,
                        caseversion: that.caseversion,
                        testplan: that.testplan,
                        model: that.model,
                        casemodel: that.casemodel,
                        key: that.key,
                        caseid: that.caseid,
                        result: that.result,
                        tester: that.tester,
                        testtime: that.testtime,
                    })
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.tableData = response.data.tableData;
                            that.$message.success(response.data.msg)
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            gettime() {
                let nowtime = new Date();
                let moment = require("moment");
                return moment(nowtime).format("YYYY-MM-DD HH:mm:ss");
            },
            cellStyle({row, rowIndex, column, columnIndex}) {
                if (column.property === 'caseresult') {
                    if (row.caseresult === 'Pass') {
                        return {
                            backgroundColor: '#00FF00'
                        }
                    } else if (row.caseresult === 'Fail') {
                        return {
                            backgroundColor: '#FF0000'
                        }
                    }
                    else if (row.caseresult === 'Block') {
                        return {
                            backgroundColor: '#FFFF00'
                        }
                    }
                    else if (row.caseresult === 'NT') {
                        return {
                            backgroundColor: '#BEBEBE'
                        }
                    }
                }
            },
            autosave(row) {
                let that = this;
                const path = this.url + "/case/autosave";
                that.caseid= row.row.id;
                that.bugid=row.row.bugid;
                that.bugremark=row.row.bugremark;
                that.bugtitle=row.row.bugtitle;
                that.project = this.project;
                that.caseversion = this.caseversion;
                that.testplan = this.testplan;
                axios
                    .post(path, {
                        project: that.project,
                        caseversion: that.caseversion,
                        testplan: that.testplan,
                        caseid: that.caseid,
                        bugid: that.bugid,
                        bugtitle: that.bugtitle,
                        bugremark: that.bugremark,
                    })
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.$message.success(response.data.msg)
                        }
                        else if(parseInt(response.data.code) === 40001){
                            that.$message.warning(response.data.msg)
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
        }
    }
</script>

<style scoped>

</style>

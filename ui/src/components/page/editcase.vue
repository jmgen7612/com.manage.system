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
                :data="tableData"
                :edit-config="{trigger: 'click', mode: 'cell'}">
            <vxe-table-column type="checkbox" width="60"></vxe-table-column>
            <vxe-table-column field="ID" title="ID" type="seq" width="60"></vxe-table-column>
            <vxe-table-column
                    sortable
                    field="caseid"
                    title="用例编号"
                    :edit-render="{name: 'input'}"
                    width="120">
            </vxe-table-column>
            <vxe-table-column
                    sortable
                    field="model"
                    title="主模块"
                    :edit-render="{name: 'input'}"
                    width="120">
            </vxe-table-column>
            <vxe-table-column
                    field="submodel"
                    title="子模块"
                    :edit-render="{name: 'input'}"
                    width="120">
            </vxe-table-column>
            <vxe-table-column
                    sortable
                    field="level"
                    title="级别"
                    :edit-render="{name: 'input'}"
                    width="120">
            </vxe-table-column>
            <vxe-table-column
                    field="preconditions"
                    title="前提条件"
                    :edit-render="{name: 'input'}"
                    width="120">
            </vxe-table-column>
            <vxe-table-column
                    field="title"
                    title="标题"
                    :edit-render="{name: 'input'}"
                    width="120">
            </vxe-table-column>
            <vxe-table-column
                    field="step"
                    title="步骤"
                    :edit-render="{name: 'input'}"
                    width="300">
            </vxe-table-column>
            <vxe-table-column
                    field="expectresult"
                    title="期待结果"
                    :edit-render="{name: 'input'}"
                    width="120">
            </vxe-table-column>
            <vxe-table-column
                    field="remark"
                    title="备注"
                    :edit-render="{name: 'input'}">
            </vxe-table-column>
            <vxe-table-column title="操作" width="180" show-overflow>
                <template v-slot="{ row }">
                    <vxe-button style="background: #FFFF00" name="update" @click="update(row,$event)">更新</vxe-button>
                    <vxe-button style="background: #FF0000" name="remove" @click="remove(row,$event)">删除</vxe-button>
                </template>
            </vxe-table-column>
        </vxe-table>
    </div>
</template>

<script>
        import axios from "axios";
    export default {
        name: "editcase",
        data() {
            return {
                url: process.env.VUE_APP_URL,
                project: '',
                caseversion: '',
                model: '',
                key: '',
                tableData: [],
                caseversionview: [],
                modelview: [],

                projects: [],
                caseversions: [],
                models: [],
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
                that.modelview = [];
                that.model = '';
                that.j = 0;
                if (val.length !== 0) {
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
            onSubmit() {
                let that = this;
                that.project = this.project;
                that.caseversion = this.caseversion;
                that.model = this.model;
                that.key = this.key;
                const path = this.url + "/case/querycase";
                axios
                    .post(path, {
                        project: that.project,
                        caseversion: that.caseversion,
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
            update(row, event) {
                let that = this;
                const path = this.url + "/case/updatecase";
                that.caseinfo = row;
                axios
                    .post(path, {
                        caseinfo: that.caseinfo,
                    })
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.$message.success(response.data.msg)
                        }
                        else if(parseInt(response.data.code) === 40001) {
                            that.$message.error(response.data.msg)
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            remove(row, event) {
                let that = this;
                const path = this.url + "/case/removecase";
                that.caseinfo = row;
                axios
                    .post(path, {
                        caseinfo: that.caseinfo,
                    })
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.$message.success(response.data.msg)
                        }
                        else if(parseInt(response.data.code) === 40001) {
                            that.$message.error(response.data.msg)
                        }
                    })
                    .catch(function (error) {
                        console.log(error)
                    })
            },
            datainfo() {
                let that = this;
                const path = this.url + "/case/datainfo";
                axios
                    .get(path)
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.projects = response.data.projects;
                            that.caseversions = response.data.caseversions;
                            that.models = response.data.models
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

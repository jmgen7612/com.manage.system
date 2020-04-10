<template>
    <div>
        <div>
            <span>用例文件导入：</span><br>
            <el-upload
                    class="upload-demo"
                    ref="upload"
                    :multiple='false'
                    :auto-upload='false'
                    :show-file-list='true'
                    :with-credentials="true"
                    list-type='text'
                    accept=".xls,.xlsx"
                    :limit="1"
                    :on-preview="handlePreview"
                    :on-remove="handleRemove"
                    :on-success="uploadFileSuccess"
                    :on-error="uploadFileError"
                    :on-change="fileChange"
                    :on-exceed="handleExceed"
                    :file-list="fileList"
                    action>
                <el-button slot="trigger" size="small" type="primary">选择用例文件</el-button>
                <el-button style="margin-left: 10px;" size="small" type="success" @click="uploadFile">导入用例</el-button>
                <div class="el-upload__tip" slot="tip">一次只能上传一个文件，仅限excel文件，单文件不超过1MB</div>
                <div class="el-upload__tip" slot="tip">规范的文件名称是：用例文件名称_版本号_项目名称</div>
                <br>
            </el-upload>
            <br>
        </div>
        <div>
            <vxe-toolbar>
                <template v-slot:buttons>
                    <vxe-button icon="fa fa-plus" @click="insertEvent(-1)">新增用例</vxe-button>
                    <vxe-button @click="$refs.xTable.removeCheckboxRow()">删除选中</vxe-button>
                </template>
            </vxe-toolbar>
            <vxe-table
                    border
                    resizable
                    style="width: 100%"
                    show-overflow
                    ref="xTable"
                    class="my_table_insert"
                    :edit-config="{trigger: 'click', mode: 'cell'}">
                <vxe-table-column type="checkbox" width="60"></vxe-table-column>
                <vxe-table-column field="ID" title="ID" type="seq" width="60"></vxe-table-column>
                <vxe-table-column
                        sortable
                        field="project"
                        title="项目名称"
                        :edit-render="{name: 'input'}"
                        width="120">
                </vxe-table-column>
                <vxe-table-column
                        sortable
                        field="version"
                        title="用例版本"
                        :edit-render="{name: 'input'}"
                        width="120">
                </vxe-table-column>
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
                        width="200">
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
                        <vxe-button style="background: #FFFF00" name="save" @click="save(row,$event)">保存</vxe-button>
                    </template>
                </vxe-table-column>
            </vxe-table>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "addcase",
        data() {
            return {
                fileList: [],   // excel文件列表
                tableData: [],
                url: process.env.VUE_APP_URL
            }
        },
        methods: {
            uploadFileRequest(url, params) {
                return axios({
                    method: 'post',
                    url: `${url}`,
                    data: params,
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
            },
            // 上传文件个数超过定义的数量
            handleExceed(files, fileList) {
                this.$message.warning(`当前限制选择 1 个文件，请删除后继续上传`)
            },
            handleRemove(file, fileList) {
                console.log(file, fileList);
                this.fileList = [];
                this.$message.success('文件删除成功');
            },
            handlePreview(file) {
                console.log(file);
            },
            // 文件状态改变时的钩子
            fileChange(file) {
                const extension = file.name.split('.')[file.name.split('.').length - 1];
                let size = file.size / 1024 / 1024;
                if (extension !== 'xlsx' && extension !== 'xls') {
                    this.$message.warning('只能上传后缀是.xlsx和.xls的文件');
                }
                if (size > 5) {
                    this.$message.warning('文件大小不得超过5M');
                }
                this.fileList.push(file.raw);
            },
            // 文件上传成功时的钩子
            uploadFileSuccess(res) {
                console.log(res);
                this.$message.success('文件上传成功');
            },
            // 文件上传失败时的钩子
            uploadFileError(err, file, fileList) {
                console.log(err);
                this.$message.error('文件上传失败');
            },
            // 上传文件
            uploadFile() {
                let that = this;
                if (that.fileList.length === 0) {
                    this.$message.warning('请先选择文件');
                } else {
                    const path = this.url + "/case/uploadcase";
                    const form = new FormData();
                    form.append('file', that.fileList[0]);
                    form.append('name', that.fileList[0].name);
                    // axios
                    //     .post(path, {
                    //         headers: {
                    //             'Content-Type': 'multipart/form-data'
                    //         },
                    //         data: form
                    //     })
                    that.uploadFileRequest(path, form)
                        .then(function (response) {
                            console.log(response.data);
                            if (parseInt(response.data.code) === 200) {
                                that.$message.success(response.data.msg);
                            }
                            else if (parseInt(response.data.code) === 40001) {
                                console.log(response);
                                // 提示信息
                                that.$message.error(response.data.msg);
                            }
                            else if (parseInt(response.data.code) === 40002) {
                                console.log(response);
                                // 提示信息
                                that.$message.error(response.data.msg);
                            }
                        })
                        .catch(function (error) {
                            console.log(error);
                            that.$message.error('文件上传失败');
                        })
                }
            },

            async insertEvent(row) {
                let record = {};
                let {row: newRow} = await this.$refs.xTable.insertAt(record, row);
                await this.$refs.xTable.setActiveCell(newRow)
            },
            save(row, event) {
                let that = this;
                const path = this.url + "/case/addcase";
                that.caseinfo = row;
                axios
                    .post(path, {
                        caseinfo: that.caseinfo,
                    })
                    .then(function (response) {
                        if (parseInt(response.data.code) === 200) {
                            that.$message.success(response.data.msg)
                        }
                        else if (parseInt(response.data.code) === 40001) {
                            that.$message.error(response.data.msg)
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

<template>
    <div class="login-wrap">
        <div class="login">
            <div>
                <h1 class="title">欢迎登录测试管理平台</h1>
                <el-form class="login_form">
                    <el-form-item prop="username">
                        <label>账户:</label>
                        <el-input type="text" v-model="username" placeholder="请输入用户名或邮箱">
                            <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <label>密码:</label>
                        <el-input type="password" v-model="password" placeholder="请输入密码">
                            <el-button slot="prepend" icon="el-icon-lock"></el-button>
                        </el-input>
                    </el-form-item>
                </el-form>
                <div class="login_btn">
                    <el-button type="primary" @click="login">登录</el-button>
                </div>
                <p style="color: #000099">没有账号<el-link style="float: right; font-size: 16px;color: #000099" @click="toregister">去注册</el-link></p>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: 'login',
        data: function () {
            return {
                username: '',
                password: '',
                url:process.env.VUE_APP_URL
            }
        },
        methods: {

            login: function () {
                let that = this;
                const message = this.$message;
                const path = this.url+"/auth/login";
                if (that.username !== "") {
                    if (that.password !== "") {
                        axios
                            .post(path, {
                                username: that.username,
                                password: that.password
                            })
                            .then(function (response) {
                                // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
                                // 可以直接通过 response.log 取key-value
                                // 坑一：这里不能直接使用 this 指针，不然找不到对象
                                // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
                                if (parseInt(response.data.code) === 400) {
                                    // 登录失败
                                    that.username = '';
                                    that.password = '';
                                }
                                else if (parseInt(response.data.code) === 200) {
                                    // 存token
                                    sessionStorage.setItem('token', response.data.token);
                                    localStorage.setItem('username', response.data.username);
                                    localStorage.setItem('gravatar', response.data.gravatar);
                                    message.success('登录成功');
                                    that.$router.push('/')
                                }
                                else if (parseInt(response.data.code) === 20001) {
                                    console.log(response);
                                    // 提示信息
                                    message.error(response.data.msg);
                                }
                            })
                            .catch(function (error) {
                                console.log(error)
                            })
                    }
                    else {
                        message.error("密码不能为空！")
                    }
                }
                else {
                    message.error("用户名不能为空！")
                }
            },
            toregister: function () {
                let that = this;
                that.$router.push('register')
            },
        }
    }
</script>

<style scoped>
    .login-wrap {
        position: relative;
        width: 100%;
        height: 100%;
        background-image: url(../../assets/img/background.jpg);
        background-size: 100%;
    }

    .login {
        position: absolute;
        left: 50%;
        top: 35%;
        width: 350px;
        margin: -190px 0 0 -175px;
        border-radius: 2px;
        background: rgba(255, 255, 255, 0.3);
        overflow: hidden;
    }

    .title {
        width: 100%;
        line-height: 50px;
        text-align: center;
        color: #2c3e50;
    }

    .login_form {
        padding: 20px 20px;
    }

    .login_btn {
        text-align: center;
    }

    .login_btn button {
        width: 100%;
        height: 36px;
        margin-bottom: 10px;
    }
</style>

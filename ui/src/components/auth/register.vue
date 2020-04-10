<template>
    <div class="register-wrap">
        <div class="register">
            <div>
                <h1 class="title">注册测试管理平台</h1>
                <el-form class="register_form">
                    <el-form-item>
                        <label>用户名:</label>
                        <el-input type="text" v-model="username" placeholder="请输入用户名">
                            <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <label>邮箱:</label>
                        <el-input type="text" v-model="email" placeholder="请输入邮箱">
                            <el-button slot="prepend" icon="el-icon-message"></el-button>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <label>密码:</label>
                        <el-input type="password" v-model="password" placeholder="请输入密码">
                            <el-button slot="prepend" icon="el-icon-lock"></el-button>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <label>重复密码:</label>
                        <el-input type="password" v-model="repassword" placeholder="请重新输入密码">
                            <el-button slot="prepend" icon="el-icon-lock"></el-button>
                        </el-input>
                    </el-form-item>
                </el-form>
                <div class="register_btn">
                    <el-button type="primary" @click="register">注册</el-button>
                </div>
                <p style="color: #000099">已有账号<el-link style="float: right; font-size: 16px;color: #000099" @click="tologin">去登录</el-link></p>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: 'register',
        data: function () {
            return {
                email: '',
                username: '',
                password: '',
                repassword: '',
                url:process.env.VUE_APP_URL
            }
        },
        methods: {
            register: function () {
                let that = this;
                const path = this.url+"/auth/register";
                const message = this.$message;
                // debugger;
                let reg1 = /^[A-Za-z][A-Za-z0-9_.]*$/;
                let reg2 = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
                if (that.username !== "" && reg1.test(that.username)) {
                    if (that.email !== "" && reg2.test(that.email)) {
                        if (that.password === that.repassword) {
                            if (that.password.length < 8 || that.password.length > 20) {
                                axios
                                    .post(path, {
                                        email: that.email,
                                        username: that.username,
                                        password: that.password,
                                        repassword: that.repassword
                                    })
                                    .then(function (response) {
                                        console.log(response.data);
                                        if (parseInt(response.data.code) === 200) {
                                            message.success('注册成功');
                                            that.$router.push('login')
                                        }
                                        else if (parseInt(response.data.code) === 20005) {
                                            message.error(response.data.msg)
                                        }
                                    })
                                    .catch(function (error) {
                                        console.log(error);
                                        message.error('注册失败');
                                    })
                            }
                            else {
                                message.error("密码长度不对，长度最少8位，最大20位")
                            }
                        }
                        else {
                            message.error("两次密码输入不一致！")
                        }
                    }
                    else {
                        message.error("请输入有效的邮箱")
                    }
                }
                else {
                    message.error("请输入有效的用户名")
                }
            },
            tologin: function () {
                let that = this;
                that.$router.push('login')
            },
        }
    }
</script>

<style scoped>
    .register-wrap {
        position: relative;
        width: 100%;
        height: 100%;
        background-image: url(../../assets/img/login-bg.jpg);
        background-size: 100%;
    }

    .register {
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

    .register_form {
        padding: 20px 20px;
    }

    .register_btn {
        text-align: center;
    }

    .register_btn button {
        width: 100%;
        height: 36px;
        margin-bottom: 10px;
    }
</style>

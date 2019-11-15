// 检测用户输入是否存在，包括用户名和邮箱
$("#exampleInputEmail1").on("blur", function () {
    var email = $("#exampleInputEmail1").val();
    $.ajax(
        {
            url: "/api/v1/login/",
            type: "get",
            data: {
                email: email
            },
            success: function (ret) {
                if (ret.code === 1001) {
                    $(".email-error").text(ret.msg);
                } else {
                    $(".email-error").text("");
                }

            }
        }
    )
});

// 极验 发送登录数据的
var handlerPopup = function (captchaObj) {
    // 成功的回调
    captchaObj.onSuccess(function () {
        var validate = captchaObj.getValidate();
        // 1. 取到用户填写的用户名和密码 -> 取input框的值
        var email = $("#exampleInputEmail1").val();
        var password = $("#exampleInputPassword1").val();
        var check = $("#check").prop("checked");
        $.ajax({
            url: "/api/v1/login/", // 进行二次验证
            type: "post",
            dataType: "json",
            data: {
                email: email,
                password: password,
                check: check,
                // {#crsf_token 的验证#}
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                geetest_challenge: validate.geetest_challenge,
                geetest_validate: validate.geetest_validate,
                geetest_seccode: validate.geetest_seccode
            },
            success: function (data) {
                if (data.status) {
                    // 有错误，在页面上提示
                    $(".login-error").text(data.msg);
                } else {
                    // 登陆成功
                    location.href = data.msg;
                }
            }
        });
    });

    $("#login").click(function () {
        captchaObj.show();
    });
    // 将验证码加到id为captcha的元素里
    captchaObj.appendTo("#popup-captcha");
    // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
};
// 当input框获取焦点时将之前的错误清空
$("#exampleInputEmail1,#exampleInputPassword1").focus(function () {
    // 将之前的错误清空
    $(".login-error").text("");
});

// 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
$.ajax({
    url: "/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
    type: "get",
    dataType: "json",
    success: function (data) {
        // 使用initGeetest接口
        // 参数1：配置参数
        // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
        initGeetest({
            gt: data.gt,
            challenge: data.challenge,
            product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
            offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
            // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
        }, handlerPopup);
    }
});

// 回车键点击
$("#login-interface").on("keydown", function (event) {
    if (event.keyCode === 13) {
        $("#login").trigger("click");
    }
});
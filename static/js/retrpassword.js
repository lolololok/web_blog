var time = 60;
var flag = true;   //设置点击标记，防止60内再次点击生效
//发送验证码
$('#dyMobileButton').click(function () {
    $(this).attr("disabled", true);
    var email = $("#email").val();
    if (flag) {
        var timer = setInterval(function () {
            if (time === 60 && flag) {
                flag = false;
                $.ajax({
                    type: 'get',
                    async: false,
                    url: '/api/v1/emailva/',
                    dataType: "json",
                    data: {
                        email: email
                    },
                    success: function (data) {
                        if (data.status === 1000) {
                            $("#dyMobileButton").html("已发送");
                        } else {
                            alert(data.msg);
                            flag = true;
                            time = 60;
                            clearInterval(timer);
                        }
                    }
                });
            } else if (time === 0) {
                $("#dyMobileButton").removeAttr("disabled");
                $("#dyMobileButton").html("免费获取验证码");
                clearInterval(timer);
                time = 60;
                flag = true;
            } else {
                $("#dyMobileButton").html(time + " s 重新发送");
                time--;
            }
        }, 1000);
    }
});

// 检测用户是否注册
$("#email").on("blur", function () {
    var email = $("#email").val();
    $.ajax(
        {
            url: "/api/v1/emailcheck/",
            type: "get",
            data: {
                email: email
            },
            success: function (ret) {
                if (ret.code === 1001) {
                    $(".email-error").html(ret.msg);
                } else {
                    $(".email-error").text("");
                }

            }
        }
    )
});

// 重置密码提交各种错误信息提示
$("#reset").on("click", function () {
    var code = $("#code").val();
    var email = $("#email").val();
    var pwd = $("#pwd").val();
    var repwd = $("#repwd").val();
    $.ajax({
        url: "/api/v1/retrpwd/",
        type: "post",
        data: {
            code: code,
            email: email,
            pwd: pwd,
            repwd: repwd,
            csrfmiddlewaretoken: $('[name = "csrfmiddlewaretoken"]').val()
        },
        success: function (arg) {
            if (arg.code === 1000) {
                $(".code-error").text("");
                $(".pwd-error").text("");
                swal({
                        title: "密码重置成功是否返回首页？",
                        type: "warning",
                        showCancelButton: true,
                        confirmButtonColor: "#DD6B55",
                        confirmButtonText: "确定！",
                        cancelButtonText: "取消",
                        closeOnConfirm: false,
                        closeOnCancel: false
                    },
                    function (isConfirm) {
                        if (isConfirm) {
                            location.href = "/api/v1/index/"
                        }
                        else {
                            swal("Cancelled");
                        }
                    });
            }
            else if (arg.code === 1001) {
                $(".code-error").text(arg.msg);
                $(".pwd-error").text("");
            }
            else if (arg.code === 1002) {
                $(".code-error").text("");
                $(".pwd-error").text(arg.msg);
            }
            else if (arg.code === 1003) {
                $(".code-error").text(arg.msg);
                $(".pwd-error").text("");
            }
            else if (arg.code === 1004) {
                $(".code-error").text(arg.msg);
                $(".pwd-error").text("");
            }
            else if (arg.code === 1005) {
                alert(arg.msg);
            }
            else if (arg.code === 1006) {
                alert(arg.msg);
            }
        }
    })
});

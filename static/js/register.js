//找到头像的input标签绑定change事件
$('#id_avatar').on("change", function () {
    var filereader = new FileReader();
    //取到当前选中的文件
    filereader.readAsDataURL(this.files[0]); //读取文件需要时间
    //等上一步读完文件之后把照片加
    filereader.onload = function () {
        //把图片加载到img标签中
        $('#img-ava').attr('src', filereader.result);
    };
});

// 用户注册
$('#re-submit').on('click', function () {
    //获取用户填写的数据
    var formdata = new FormData();
    formdata.append('username', $('#id_username').val());
    formdata.append('password', $('#id_password').val());
    formdata.append('repassword', $('#id_repassword').val());
    formdata.append('email', $('#id_email').val());
    formdata.append('sign', $('#id_sign').val());
    formdata.append('csrfmiddlewaretoken', $("[name = 'csrfmiddlewaretoken']").val());
    formdata.append('img-ava', $('#id_avatar')[0].files[0]);

    $.ajax({
        url: '/api/v1/register/',
        type: 'post',
        processData: false, //告诉jQuery不要处理我的数据
        contentType: false,//告诉jQuery不要设置content类型
        data: formdata,
        success: function (data) {
            if (data.status) {
                // 显示错误
                $.each(data.msg, function (k, v) {
                    $("#id_" + k).next('span').text(v[0]).parent().parent().addClass('has-error');
                })
            } else {
                // 没错误
                location.href = data.msg;
            }
        }
    })
});

// 给username绑定失去焦点事件检测用户是否已存在
$('#id_email').on('input', function () {
    // 取到用户填写的值
    var email = $(this).val();
    $.ajax({
        url: '/api/v1/register_check/',
        type: 'get',
        data: {'email': email},
        success: function (data) {
            if (data.status) {
                // 用户已被注册
                $('#id_email').next().text(data.msg).parent().parent().addClass('has-error');
            } else {
                $('#id_email').next().text('').parent().parent().removeClass('has-error')
            }
        }
    })
});
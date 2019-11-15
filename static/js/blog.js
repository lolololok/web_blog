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

// 添加，编辑文章图片上传
KindEditor.ready(function (k) {
    window.editor = k.create('#article_content', {
        width: '900px',
        height: '600px',
        resizeType: 0,
        uploadJson: '/api/v1/upload/',
        extraFileUploadParams: {
            csrfmiddlewaretoken: $('[name = "csrfmiddlewaretoken"]').val()
        },
        filePostName: 'upload_img'
    });
});


//文章置顶
$(".toped").on("click", function () {
    var article_id = $(this).attr("id");
    $.ajax({
        url: "/api/v1/article/top/",
        type: "get",
        data: {
            article_id: article_id,
        },
        success: function (arg) {
            if (arg.code === 1001) {
                alert(arg.msg)
            }
            if (arg.code === 1000) {
                window.location.reload()
            }
        }
    })
});

//编辑文章添加文章安全提示
var flag;
var info;
var http = location.href.trim().split("/");

if (http[http.length - 2] === "addarticle" || http[http.length - 2] === "editarticle") {
    flag = true;
    if (http[http.length - 2] === "addarticle") {
        info = "你已添加完成，确定离开当前页面吗？"
    } else {
        info = "你已修改完成，确定离开当前页面吗？"
    }
} else {
    flag = false;
}
if (flag) {
    window.onbeforeunload = function (e) {
        var e = window.event || e;
        e.returnValue = (info);
    };
    window.onunload = function (ev) {
        var ev = window.event || ev;
        ev.returnValue("确定重新加载？");
    }
}

// 文章删除温馨提示
$(".blog-delete").on("click", function () {
    var article_id = $(this).attr("article-id");
    swal({
            title: "确定删除吗？",
            text: "你将无法恢复该文章！",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定删除！",
            cancelButtonText: "取消删除！",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {
            if (isConfirm) {
                $.ajax({
                    url: "/api/v1/deletearticle/?id=" + article_id,
                    type: "get",
                    success: function (arg) {
                        swal("删除！", "此文章已经被删除。", "success");
                        $("a[article-id=" + arg.article_id + "]").parent().parent().remove();
                    }
                });
            } else {
                swal("取消！", "你的文章已被保留的:)",
                    "error");
            }
        });
});
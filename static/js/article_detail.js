//点赞
$('.action').on('click', function () {
    var is_up = $(this).hasClass('diggit');
    var article_id = $(".article-info").attr("article_id");
    var skr = function (Elen) {
        var val = Elen.text();
        val = parseInt(val) + 1;
        Elen.text(val);
    };
    $.ajax({
        url: '/api/v1/article/updown/',
        type: 'post',
        data: {
            article_id: article_id,
            is_up: is_up,
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
        },

        success: function (data) {
            if (data.status) {  //赞，踩成功
                if (is_up) {
                    skr($('#digg_count'));
                } else {
                    skr($('#bury_count'));
                }
            } else { //重复提交
                $('#digg_tips').html(data.warring);
                setTimeout(function () {
                    $('#digg_tips').html('');
                }, 1000)

            }
        }
    })
});


//评论
var pid = '';
$('#comment_btn').on('click', function () {
    var article_id = $('.article-info').attr('article_id');
    var content = $('#comment_content').val();
    if (pid) {
        var index = content.indexOf('\n');
        content = content.slice(index + 1);
    }
    $.ajax({
        url: '/api/v1/article/comment/',
        type: 'post',
        data: {
            pid: pid,
            article_id: article_id,
            content: content,
            csrfmiddlewaretoken: $('[name = "csrfmiddlewaretoken"]').val()
        },
        success: function (respones) {
            var create_time = respones.create_time;
            var username = respones.username;
            var content = respones.content;
            var comment_li = '<li class="list-group-item"> <div> <span style="color: gray">' + create_time + '</span>&nbsp;&nbsp; <a href=""><span>' + username + '</span></a> <a href="" class="pull-right"><span>回复</span></a> </div> <div class="con"> <p> ' + content + '</p> </div> </li>';
            $('.comment-list').append(comment_li);
            $('#comment_content').val('');
        }
    })
});
// 子评论
// 回复按钮
$('.reply-btn').on('click', function () {
    var $Elen_com = $('#comment_content');
    $Elen_com.focus();
    var v = '@' + $(this).attr('username') + '\n';
    $Elen_com.val(v);
    // pid
    pid = $(this).attr('comment_pk');

});
    $(document).ready(function(i){
        $('body').hide().fadeIn(1000);
    })

    var tags = $(".tag");
    for (var i = tags.length - 1; i >= 0; i--) {
        tags[i].style.fontSize = random_num(1,30) + 'px';
        tags[i].style.color = random_color();
    };
    var tagCloud = $("#tagCloud");
    var boxWidth = tagCloud.width();

    tags[0].style.marginLeft = boxWidth / 2 - 50 + 'px';
    tags[2].style.clear = 'left';
    tags[2].style.marginLeft = boxWidth / 3 - 50 + 'px';
    tags[6].style.clear = 'left';
    tags[6].style.marginLeft = boxWidth / 4 - 50 + 'px';
    tags[tags.length-2].style.clear = 'left';
    tags[tags.length-2].style.marginLeft = boxWidth / 2 - 50 + 'px';
    tags[tags.length-6].style.clear = 'left';
    tags[tags.length-6].style.marginLeft = boxWidth / 3 - 50 + 'px';
    tags[tags.length-12].style.clear = 'left';
    tags[tags.length-12].style.marginLeft = boxWidth / 4 - 50 + 'px';

    $("span:not(#desc)").click(function(){
        var width = $(this).width();
        var height = $(this).height();
        var top = $(this).position().top;
        var left = $(this).position().left;
        var desc = $(this).attr('desc');

        var descObj = $("#desc");
        var iconObj = $("#icon");

        // 隐藏
        if (descObj.css('display') == 'none') {
            descObj.fadeIn(300);
            iconObj.fadeIn(300);
            // descObj.css('display', 'block');
            // iconObj.css('display', 'block');
        }else{
            if (descObj.text() != desc) {
                descObj.hide().fadeIn(300);
                iconObj.hide().fadeIn(300);
                // descObj.css('display', 'block');
                // iconObj.css('display', 'block');
            }else{
                descObj.fadeOut(100);
                iconObj.fadeOut(100);
                // descObj.css('display', 'none');
                // iconObj.css('display', 'none');
            }
        }
        descObj.text(desc);

        // 定位描述框和小三角
        var descWidth = descObj.width();
        var descHeight = descObj.height();
        descObj.css('top', top - descHeight - 30);
        var marginLeft = parseInt($(this).css('marginLeft'));
        iconObj.css('top', top - 10);

        // 左侧防超长
        if (marginLeft > 15) {
            descObj.css('left', marginLeft)
            iconObj.css('left', marginLeft + descWidth / 2 + width / 2 - 5);
        }else{
            descObj.css('left', left);
            iconObj.css('left', left + 10 + width / 2);
        }

        // 右侧防超长
        var descLeft = descObj.position().left;
        var boxPaddingLeft = parseInt(tagCloud.css('paddingLeft'));
        var boxPaddingRight = parseInt(tagCloud.css('paddingRight'));
        var descRight = descLeft + descWidth + 24;
        var boxRight = boxWidth + boxPaddingLeft + boxPaddingRight;
        if (descRight > boxRight) {
            var current_left = parseInt(descObj.css('left'));
            descObj.css('left', current_left - (descRight - boxRight))
        }

    });

    // 随机字号
    function random_num(min,max){
        return Math.floor(min+Math.random() * (max-min));
    }
    // 随机字体颜色
    function random_color(){
        return '#'+('00000'+(Math.random()*0x1000000<<0).toString(16)).slice(-6);
    }

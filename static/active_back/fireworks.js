js:
$(function(){
    var input_e=$("input");
    //javascript检测浏览器是否支持某些事件
    //typeof input["oninput"] == "undefined"

    var y=input_e.offset().top;
    var x=input_e.offset().left;
    var len=0;
    var firewNum=15;// 烟花个数
    11     // 点击页面 在鼠标位置 出现心形 烟花
    $("body").click(function(ev){
        xin(ev); // 点击心形
        Fireworks(ev)// 点击烟花
    });

    // 鼠标点击出现心形
    function xin(ev)
    {
        var color=randColor();
        var div=document.createElement("div");
            div.className='heart';
            div.style.backgroundColor=color;
            div.style.left=ev.pageX+'px';
            div.style.top=ev.pageY+'px';
            document.body.append(div);
            var i=1;
        var t=setInterval(function(){
            div.style.top=div.offsetTop-2+'px';
            i-=0.01;
            div.style.opacity=i;
            var scale=1+(1-i);
            div.style.transform='scale('+scale+','+scale+') rotate(45deg)';
            if(i<0.01 || div.style.top+div.offsetTop>=window.innerHeight)
            {
                div.remove();
                clearInterval(t);
            }
        },30)
    }

    // 随机色
    function randColor()
    {
        var r=parseInt(Math.random()*256);
        var g=parseInt(Math.random()*256);
        var b=parseInt(Math.random()*256);
        var a=Math.random().toFixed(1)
        var color='rgba('+r+','+g+','+b+','+a+')';
        return color;
    }

    // 创建烟花
    function Fireworks(ev)
    {
        // 烟花一种颜色-- 90去掉注释
        /*var color=randColor();
        for(var i=0;i<firewNum;i++)
        {
            create(ev,color);
        }*/
        for(var i=0;i<firewNum;i++)
        {
            create(ev,null);
        }
    }

    function create(ev,color)
    {// 操作元素使用的 原生 js ,使用jquery 失败 取不到元素
        var div=document.createElement("div");
            div.className='Fireworks';
            div.style.backgroundColor=randColor();
        //    div.style.backgroundColor=color;
            div.style.left=ev.pageX+'px';
            div.style.top=ev.pageY+'px';
            document.body.append(div);
            var i=1;
            // 正负 -5右     +5左
            var speedX =(parseInt(Math.random()*2) == 0 ? 1 : -1)*parseInt(Math.random()*5 + 1);
            // 向上 -0--17
            var speedY=-parseInt(Math.random()*18);

            var time=setInterval(function()
            {
                ++i;
                var left=div.offsetLeft+speedX;
                var top=div.offsetTop+speedY+i;
                 // 加 i top 越来越大， 烟花下落，否则烟花向上飘 每次获取得div.offsetTop越来越大 速度越来越慢
                div.style.left=left+'px';
                div.style.top=top+'px';
                if(div.offsetLeft+div.offsetWidth>window.innerWidth || div.offsetLeft<2 || div.offsetTop+div.offsetHeight>window.innerHeight || div.offsetTop<2 )
                {
                    //如果超出屏幕 移除div 关闭定时器
                    div.remove();
                    clearInterval(time);
                }

            },40)
    }
});
//简易的js框架
//Used by 胡晓帆

//简单的选择器,有仿jqury的attr功能
var $=function(id){
	var obj=document.querySelectorAll(id);
    if(obj.length==1)
        return obj[0];
    else
        return obj;
}
//返回顶部 speed为16ms向上滚动的距离;即滚动的速度,cancelAnimationFrame默认60帧
function gotop(speed){  
	var timer=null;
    speed = speed ? speed : 100;  //默认100
	cancelAnimationFrame(timer);
    timer = requestAnimationFrame(function fn(){
    var oTop = document.body.scrollTop || document.documentElement.scrollTop;
    if(oTop > 0){
    	if(oTop < 900&&speed>5.5){
    		speed=speed-5.5;
    	}
    	//console.log(speed+":"+oTop);
        document.body.scrollTop = document.documentElement.scrollTop = oTop - speed;
        timer = requestAnimationFrame(fn);
    }  
    else{
        cancelAnimationFrame(timer);
        } 
    });
}
//仿jq简单封装ajax 带callback功能;
function ajax(opt) {
        opt = opt || {};
        opt.type = opt.type == null? 'get':opt.type;
        opt.url = opt.url || '';
        if(opt.url=='')
            alert("重要参数未填->url");
        opt.async = opt.async || true;
        opt.data = opt.data || null;
        opt.dataType = opt.dataType|| 'html';
        opt.callback = opt.callback||'callback';
        opt.cbname = opt.cbname||'backdata';
        opt.success = opt.success || function () {};
        opt.error = opt.error || function () {};
        opt.contentType=opt.contentType!=null ? opt.contentType:true;
        opt.processData=opt.processData!=null ? opt.processData:true;
        var xmlHttp = null;
        var params = [];
        for (var key in opt.data){
            params.push(key + '=' + opt.data[key]);
        }
        var postData = params.join('&');     //字符串拼接
        if(opt.dataType.toUpperCase() === 'JSONP'){
            window[opt.cbname]=function(result){
                opt.success(result);
            };
            var head=document.getElementsByTagName("head")[0]
            var JSONP=document.createElement("script");
            if(opt.callback!=''&&opt.cbname!='')
            opt.url = postData == '' ? opt.url:(opt.url+"?"+postData+"&");
            if(opt.url.indexOf("?")!=-1)
                JSONP.src=opt.url+"&"+opt.callback+"="+opt.cbname;
            else
                JSONP.src=opt.url+"?"+opt.callback+"="+opt.cbname;
            head.appendChild(JSONP);
            setTimeout(function(){head.removeChild(JSONP);},5000);
        }
        else{
            if (XMLHttpRequest) {
                xmlHttp = new XMLHttpRequest();
            }
            else {
                xmlHttp = new ActiveXObject('Microsoft.XMLHTTP');
            }
            if (opt.type.toUpperCase() === 'POST') {
                xmlHttp.open(opt.type, opt.url, opt.async);
                if(opt.contentType!=false)
                    xmlHttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded;charset=utf-8');
                    opt.processData==false ? xmlHttp.send(opt.data): xmlHttp.send(postData);
            }
            else if (opt.type.toUpperCase() === 'GET') {
                opt.url = postData == '' ? opt.url:opt.url+"?"+postData;   //判断是否有data,无data不需要问号
                xmlHttp.open(opt.type, opt.url, opt.async);
                xmlHttp.send();
            } 
            xmlHttp.onreadystatechange = function () {              //3次状态的改变
                //console.log(xmlHttp.readyState+""+xmlHttp.status);
                var response=xmlHttp.responseText;
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
                    response = opt.dataType == "json" ? JSON.parse(response):response;
                    opt.success(response);
                }
                else
                    if(xmlHttp.readyState ==4 && xmlHttp.status>399)
                    opt.error();
                }
        }
        }
//时间戳转换成时间;
function getDate(time) {
    if(time){
        if(Number.isInteger(time))
            time=time+"";
        time = time.length == 10 ? time*1000 : time;   //时间戳为10位需*1000，时间戳为13位的话不需乘1000
    }
    var date = time ? new Date(time):new Date(); 
    Y = date.getFullYear() + '-';
    M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
    D = date.getDate() ;
    D = D<10?"0"+D:D;
    D = D+ ' ';
    h = date.getHours();
    h = h<10?"0"+h:h;
    h = h + ':';
    m = date.getMinutes();
    m = m<10 ? "0"+m:m;
    m = m + ':';
    s = date.getSeconds();
    s=s<10?"0"+s:s;
    return Y+M+D+h+m+s;
    }
function message(content){
    if(!window.now_color)
        window.now_color="#44B78B";
    if($("head style").innerHTML.indexOf(".message")==-1){
        $("head style").innerHTML+=".message{width:200px;height:25px;position:fixed;top:12%;left:calc(50% - 100px);color:white;background:"+now_color+";text-align: center;opacity: 0;font-weight: 300;font-size: 13px;line-height: 25px;transition: 0.3s;z-index:99999}";
    }
    var mes=document.createElement("div");
    $("body").appendChild(mes);
    mes.className="message";
    mes.innerHTML=content;
    setTimeout(function(){mes.style.top="17%";mes.style.opacity="0.9"},300);
    setTimeout(function(){mes.style.opacity=0},2000);
    setTimeout(function(){$("body").removeChild(mes);},2000);
}
HTMLElement.prototype.attr=function(key,value){
    if(value==null)
        return this.attributes[key].value;
    else if(value=="")
        return this.removeAttribute(key);
    else
        return this.setAttribute(key, value);
}
$.print=function(n){
    console.log(n);
}
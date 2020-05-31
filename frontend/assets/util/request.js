
post = function (url, data, successfunction) {
    $.ajax({
        type: "post",
        url: url,
        dataType: "json",
        data: data,
        async: false,
        success: successfunction
    });
};

request_get = function (url, data, successfunction) {
    $.ajax({
        type: "get",
        url: url,
        dataType: "json",
        data: data,
        async: false,
        success: successfunction
    });
};

redirect_login = function () {
    $.ajax({
        type: "get",
        url: "/auth/test_cookie",
        dataType: "json",
        async: false,
        success: function (d) {
            if(d.status == 302){
               window.location.replace(d.url);
            }
        }
    });
}

getParams = function (key) {
     var reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if (r != null) {
        return unescape(r[2]);
     }
     return null;
};
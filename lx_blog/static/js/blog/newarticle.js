function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // 向后端获取信息
    $.get("/api_v1/category", function (resp) {
        if (resp.errno == "0") {
            var categorys = resp.data;
            for (i=0; i<categorys.length; i++) {
                 var category = categorys[i];
                 $("#category-id").append('<option value="'+ category.aid +'">'+ category.aname +'</option>');
            }
        }else {
            alert(resp.errmsg);
        }

    }, "json");

    $("#form-article-info").submit(function (e) {
        e.preventDefault();

        // 处理表单数据
        var data = {};
        $("#form-article-info").serializeArray().map(function(x) { data[x.name]=x.value });



        // 向后端发送请求
        $.ajax({
            url: "/api_v1/articles/info",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "4101") {
                    // 用户未登录
                    location.href = "/login.html";
                } else if (resp.errno == "0") {
                    // 隐藏基本信息表单
                    $("#form-article-info").hide();
                    // 显示图片表单
                    $("#form-article-image").show();
                    // 设置图片表单中的article_id
                    $("#article-id").val(resp.data.article_id);
                    location.href = "/myarticle.html";
                } else {
                    alert(resp.errmsg);
                }
            }
        })

    });

})
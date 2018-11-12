function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // 获取详情页面要展示的文章编号
    var queryData = decodeQuery();
    var articleId = queryData["id"];

    // 获取该文章的详细信息
    $.get("/api_v1/articles/" + articleId, function(resp){
        if ("0" == resp.errno) {
            $(".detail-con").html(template("article-detail-tmpl", {article:resp.data.article}));
        }
    })
})
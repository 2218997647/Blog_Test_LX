
$(document).ready(function(){
    $.get("/api_v1/user/articles", function(resp){
        if ("0" == resp.errno) {
            $("#articles-list").html(template("articles-list-tmpl", {articles:resp.data.articles}));
        } else {
            $("#articles-list").html(template("articles-list-tmpl", {articles:[]}));
        }
    });
})
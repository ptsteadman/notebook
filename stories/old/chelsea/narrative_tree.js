$(document).ready(function(){

    $(".narrative_tree>.node").show();
    
    var liveText = function(nid){
        console.log(nid);
        var text = root.find(".node[data-nid=\"" + nid + "\"]").html();
        var liveText = $("<div class='live_text'>").html(text);
        liveText.attr('data-nid', nid).hide();
        return liveText;
    }

    var showLiveText = function(nid){
        $(".live_text[data-nid=\"" + nid + "\"]").fadeIn();
        $(".live_text[data-nid=\"" + nid + "\"]").css("background-color","#fff");
    }

    var root = $(".narrative_tree").clone();
    $(".narrative").html(liveText('root').show());
    $(".narrative").on("click",".link", function(){
        var nid = $(this).attr('data-nid');
        var newText = liveText(nid);
        $(".live_text").css("background-color", "#eee");
        $(".center").css("background-color", "#eee");
        $(".replace[data-nid=\"" + nid + "\"]").fadeOut(500, function(){
            $(".replace[data-nid=\"" + nid + "\"]").replaceWith(newText);
            showLiveText(nid);
        });
        console.log($(".live_text"));
    });

});

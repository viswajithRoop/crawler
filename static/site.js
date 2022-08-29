function main() {
    console.log("Hello world! I am loaded!");
    $("a.songLink").click(function (ev) {
        console.log(ev);
        $("div.lyrics").text("Loading ... ");
        url = ev.target.href.replace("/song/","/lyrics/");
        $.ajax({url : url,
                success: function(data, textStatus, jqXHR) {
                    console.log("Succeeded");
                    $("div.lyrics").html(data);
                },
                
                
            });
        ev.preventDefault();
        });
}
$(main);


function build_lyrics(song){
    ret = $(`<p>
    <h4> Lyrics for ${song.name} </h4>
    <h5> <small class="text-muted">${song.artist.name}</small> </h5>
</p>
<p>
    ${song.lyrics}
</p>`)
    return ret;
}

function main() {
    console.log("Hello world! I am loaded!");
    $("a.songLink").click(function (ev) {
        console.log(ev.target.href);
        $("div.lyrics").text("Loading ... ");
        $.ajax({url : ev.target.href,
                dataType: 'json',
                success: function(data, textStatus, jqXHR) {    
                    console.log(data)
                    $("div.lyrics").html(build_lyrics(data.song));
                },    
            });
        ev.preventDefault();
        });
}
$(main);


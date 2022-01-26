class Game2 {
    player;

    constructor(player) {
        this.player = player;
    }

    static randomRectangle() {
        const margin = 1;
        const maxwidth = 12;
        const maxheight = 12;
        var x = margin + Math.random()*(100-margin*2-maxwidth);
        var y = margin + Math.random()*(100-margin*2-maxheight);
        var width = 3+Math.random()*maxwidth;
        var height = 3+Math.random()*maxheight;
        $("#rectangle").css("width", width+"%");
        $("#rectangle").css("height", height+"%");
        $("#rectangle").css("top", x+"%");
        $("#rectangle").css("left", y+"%");
    }

    setTimer(n) {
        $("#timer").attr("max", n);
        $("#timer").attr("count", n);
        $("#timer").text(n);
    }

    tick() {
        var n = $("#timer").attr("count");
        n-=1;
        if(n==0) {
            Game2.randomRectangle();
            $("#timer").attr("count", $("#timer").attr("max"));
        } else {
            $("#timer").attr("count", n);
        }
        $("#timer").text($("#timer").attr("count"));
    }

    updateClicks() {
        $.ajax({
            url: 'http://localhost:8080/player/'+this.player,
            dataType: 'json',
            contentType: 'application/json',
            type: 'GET',
            crossDomain: true,
            success: this.setClicks
        });
    }

    setClicks(data) {
        document.title = data['name'] + " -> " + data['clicks'] + " v0.2";
        $("#player").text(data['name']);
        $("#clicks").text(data['clicks']);
    }

    addClicks(n) {
        var data = JSON.stringify({"clicks" : n });
        $.ajax({
            url: 'http://localhost:8080/addclicks/'+this.player,
            dataType: 'json',
            contentType: 'application/json',
            type: 'POST',
            data: data,
            crossDomain: true,
            success: this.setClicks
        });
    }
}

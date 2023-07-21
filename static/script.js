//set a handler for loading the high score and game total from the session
async function loadScores(){
    let results = await axios.get("/scores");
    console.log(results);
    $("#games-played").text(results.data.gamesPlayed+" games played")
    $("#highscore").text("High Score: " + results.data.highscore)
}
loadScores();

//start a timer once the page loads, counting down 60 seconds to disable the submit button
secLeft = 60;
let intervalID =setInterval(async () => {
    if(secLeft>0) $("#timer").text("There are " + secLeft + " seconds left");
    else{
        $("#timer").text("Out of time");
        clearInterval(intervalID);
        //send metadata to server
        await axios.post("/scores", {score:$("#score").text()});
    } 
    secLeft--;
}, 1000);

//submit the question to the route defined in app.py and get a response validating the guess
document.querySelector("form").addEventListener("submit", async (e)=>{
    e.preventDefault();
    word = $("#guess").val()
    if(secLeft>0){
        let response = await axios.post("/submit", {guess:word});
        console.log(response.data);
        resElement = $("#response");
        score = $("#score");
        switch(response.data.result){
            case "not-on-board":
                resElement.text("Guess is not on the board");
                break;
                case "ok":
                resElement.text("Score increased");
                score.text(parseInt(score.text())+response.data.result.length+1);
                break;
            case "not-word":
                resElement.text("Guess is not a word");
                break;
            case "already-guessed":
                resElement.text("Word already guessed");
                break;
            default:
                resElement.text("Default code run because the result is " + response.data.result)
        }

        $("#guess").val("");
    }   
})
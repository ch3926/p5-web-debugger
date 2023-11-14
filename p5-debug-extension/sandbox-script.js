window.addEventListener('message', async function (event) {

    let newData = `${event.data.trim().replace(/[\u200B-\u200D\uFEFF]/g, '')}`

    window.frameCounter = 0

    // let data2 = data.trim().replace(/[\u200B-\u200D\uFEFF]/g, '').split(/[\s,\t,\n]+/).join(' ');
    
    // console.log(newData);
    // console.log(data2);
    // for(let i = 0; i < newData.length; i++) {
    //     if(newData.charAt(i) != data2.charAt(i)) {
    //         console.log("NOT EQUAL: \"" + newData.charAt(i) + "\" != \"" + data2.charAt(i) + "\"" + i);
    //         console.log(newData.charCodeAt(i))
    //     } else {
    //         console.log("Equal: \"" + newData.charAt(i) + "\" == \"" + data2.charAt(i) + "\"" + i);
    //     }
    // }
    let customNoiseSeed = Math.floor(Math.random() * 1000)
    let customRandomSeed = Math.floor(Math.random() * 1000)
    let noDrawScript = newData.replace(`function draw`, `function p5Draw`).replace(`function p5Setup(){`, `function p5Setup(){noiseSeed(${customNoiseSeed});randomSeed(${customRandomSeed});`);

    // noDrawScript = noDrawScript.replace(`function setup {`, `function setup {noiseSeed(${customNoiseSeed});randomSeed(${customRandomSeed})`);

    noDrawScript += `\nfunction keyPressed(){
        if(keyCode === RIGHT_ARROW) {
            p5Draw();
            window.frameCounter++;
        } else if(keyCode === LEFT_ARROW) {
            p5Setup();
            window.frameCounter--;
            for(let i = 0; i < window.frameCounter; i++) {
                p5Draw();
            }
            
        }\n
    }`

    console.log(noDrawScript);

    var newScript = document.createElement("script");
    newScript.text = noDrawScript;
    newScript.async = false;

    var newScript2 = document.createElement("script");
    newScript2.src = 'p5.min.js';
    newScript2.async = false;

    document.body.appendChild(newScript);
    document.body.appendChild(newScript2);
    
});



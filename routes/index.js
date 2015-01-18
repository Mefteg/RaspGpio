var express = require('express');
var router = express.Router();

var fs = require('fs');
var exec = require('child_process').exec;

var child = null;

/* GET home page. */
router.get('/', function(req, res) {
    res.render('index', { title: 'Express' });
});

router.post('/', function(req, res) {
    console.log("- New script received...");
    // kill the child process if it's running
    try {
        // save file content into the script file
        var writeOptions = {
            encoding: 'UTF-8',
            flag: 'w'
        };
        fs.writeFileSync("script.js", req.body.file_content, writeOptions);
        console.log("-- File content saved into script.js.");


        // execute the script trough Nodejs
        if (child === null) {
            console.log("-- No script is running, launch a new one now...");
            launchScript();
        } else {
            console.log("-- A script is running, kill it...");
            // ask to launch the new script once the current one will be dead
            child.on('exit', function() {
                console.error("+++ Child: on 'exit'...");
                child = null;
                launchScript();
            });
            // kill it
            child.kill();
        }
    } catch(error) {
        console.error(error);
    }

    res.end("OK");
});

function launchScript() {
    child = exec("node script.js", null, function(error, stdout, stderr) {
        if (error) {
            console.error("+++ Child:");
            console.error(error);
        } else {
            if (stdout) console.log("+++ Child(stdout): \n" + stdout);
            if (stderr) console.error("+++ Child(stderr): \n" + stderr);
        }

        child = null;
        console.log("+++ Child: I'm dead");
    });

    console.log("-- The script is running...");
}

module.exports = router;

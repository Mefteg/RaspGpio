//!@address http://localhost:3000/
//!@address http://10.0.1.45:3000/

var fs = require('fs');


alive();

function alive() {
    fs.writeFileSync("test.txt", "alive2\n", {flag: 'a'});

    setTimeout(alive, 5000);
}
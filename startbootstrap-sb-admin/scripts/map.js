var mysql = require('mysql');
const fs = require('fs')

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "1229",
  database: "electri"
});
con.connect( async function(err) {
    if (err) throw err; 
    while (1){
        con.query("SELECT * FROM car_matches", function (err2, result, fields) 
        {
            if (err2) throw err2;
            data = {
                'matches':[]
            }
            for (let i = 0; i < result.length; i++) {
                match = {
                    'id':result[i].id,
                    'x_coord':result[i].x_coord,
                    'y_coord':result[i].y_coord,
                    'image_name':result[i].image_name,
                    'time':result[i].timestamp,
                }
                data['matches'].push(match)
            }
            const content = JSON.stringify(data);

            fs.writeFile('dist/test.json', content, err3 => 
            {
                if (err3) {
                console.error(err3)
                return
                }
            })
            
        });
        await sleep(2000);

    }
});
           


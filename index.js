const express = require('express')
const {spawn} = require('child_process')
const app = express()
const port = 3000
const bodyParser = require('body-parser');

// use to parse json body in post request
app.use(bodyParser.json());
// define static sources
app.use(express.static(process.cwd()+"/static"));
app.use(express.static(process.cwd()+"/rars"));

app.get('/', (req, res) => {
	res.sendFile(process.cwd()+"/static/index.html")
})


app.get('/api', (req, res) => {
	url = req.query.url;
	
	var dataToSend;
	 // spawn new child process to call the python script
	const python = spawn('python', ['python/demo.py', url]);
	// You need to remove the listeners exec installs to add to the buffered stdout and stderr, 
	// even if you pass no callback it still buffers the output. 
	// Node will still exit the child process in the buffer is exceeded in this case.
	python.stdout.removeAllListeners("data");
	python.stderr.removeAllListeners("data");
	 // collect data from script
	python.stdout.on('data', function (data) {
	  	console.log('Pipe data from python script ...');
	  	dataToSend = data.toString();
	});
	// in close event we are sure that stream from child process is closed
	python.on('close', (code) => {
		console.log(`child process close all stdio with code ${code}`);
	 // send data to browser
		console.log(dataToSend)
		res.setHeader('Content-Type', 'application/json');
		if (dataToSend) dataToSend.trim();
		res.json({ "message": dataToSend , "code": code });
	});

})

app.get('/rars', function(req, res){
	fileName = req.query.file
	const file = `${__dirname}/rars/${fileName}`;
	res.download(file); // Set disposition and send it.
});

app.get('*', (req, res) => {
	res.redirect("/");
})


app.listen(process.env.PORT || port , () => console.log(`Example app listening`))
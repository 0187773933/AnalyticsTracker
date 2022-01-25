# Analytics Tracking Server

```
cp config_example.json config.json
```

- `nano config.json`
- `./dockerBuild.sh`
- `./dockerRun.sh`


- `uuid`
- `<img src='https://ta.example.com/t/$SOME_UUID' alt=''>`
- or
```
try {
	let img_1 = document.createElement( "img" );
	img_1.setAttribute( "src" , "https://ta.example.com/t/$SOME_UUID?v=" + ( new Date() ).getTime() );
	img_1.style.display = "none";
	document.body.appendChild( img_1 );
} catch( e ) {}
```
- https://ta.example.com/a/$SOME_UUID
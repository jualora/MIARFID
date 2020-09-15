/**
 * LucesTexturas.js
 * Carga un grafo de escena en Threejs, con iluminación, sombras y diferentes tipos de texturas
 *
 */

var renderer, scene, camera;

var angulo = 0;
var cuboEsfera;

var video, videoImage, videoImageContext, videoTexture;

var cameraControls;

init();
loadScene();
render();

function init() {
    //Inicializar Threejs
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0x0000AA));
    renderer.shadowMap.enabled = true;
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 100);

    camera.position.set(0.5, 2, 5);
    camera.lookAt(new THREE.Vector3(0,0,0));

    cameraControls = new THREE.OrbitControls(camera, renderer.domElement);
    cameraControls.target.set(0,0,0);

    //Luces
    var ambiental = new THREE.AmbientLight(0x444444);
    scene.add(ambiental);

    var puntual = new THREE.PointLight('white', 0.3);
    puntual.position.y = 5;
    scene.add(puntual);

    var direccional = new THREE.DirectionalLight('white', 0.3);
    direccional.position.set(-2, 3, 10);
    scene.add(direccional);

    var focal = new THREE.SpotLight('white', 0.5);
    focal.position.set(3, 3, -8);
    focal.target.position.set(0,0,0);
    focal.angle = Math.PI / 7;
    focal.penumbra = 0.2;

    focal.shadow.camera.near = 3;
    focal.shadow.camera.far = 15;
    focal.shadow.camera.fov = 40;
    focal.shadow.mapSize.width = 1024;
    focal.shadow.mapSize.height = 1024;
    
    scene.add(focal.target);
    scene.add(new THREE.CameraHelper(focal.shadow.camera));

    focal.castShadow = true;
    scene.add(focal);

}

function loadScene() {
    //Texturas
    var path = "images/";
    var txSuelo = new THREE.TextureLoader().load(path + "r_256.jpg");
    txSuelo.wrapS = txSuelo.wrapT = THREE./*RepeatWrapping*/MirroredRepeatWrapping;
    txSuelo.repeat.set(2,2);

    var txCubo = new THREE.TextureLoader().load(path + "wood512.jpg");

    var txEsfera = new THREE.TextureLoader().load(path + "Earth.jpg");

    var paredes = [path + "posx.jpg", path + "negx.jpg", path + "posy.jpg", path + "negy.jpg", path + "posz.jpg", path + "negz.jpg"];

    var mapaEntorno = new THREE.CubeTextureLoader().load(paredes);
    
    //Materiales

    var mate = new THREE.MeshLambertMaterial({color:'red', wireframe:false, map:txCubo});
    var pulido = new THREE.MeshPhongMaterial({color:'white', specular:0x99BBFF,shininess:50, envMap:mapaEntorno});
    var matSuelo = new THREE.MeshLambertMaterial({color:'white', wireframe:false, map:txSuelo});
    
    //Carga la escena

    var geoCubo = new THREE.BoxGeometry(2, 2, 2);
    var geoEsfera = new THREE.SphereGeometry(0.8, 30, 30);
    var matCubo = new THREE.MeshBasicMaterial({color: 'yellow', wireframe: true});
    
    var cubo = new THREE.Mesh(geoCubo, mate);
    cubo.position.set(1.5, 0, 0);
    cubo.receiveShadow = true;
    cubo.castShadow = true;

    cubo.add(new THREE.AxesHelper(1.5));

    var esfera = new THREE.Mesh(geoEsfera, pulido);
    esfera.position.set(-1, 0,0);
    esfera.receiveShadow = true;
    esfera.castShadow = true;

    cuboEsfera = new THREE.Object3D();
    
    cuboEsfera.add(cubo);
    cuboEsfera.add(esfera);
    cuboEsfera.position.y = 1.1;
    
    scene.add(cuboEsfera);

    scene.add(new THREE.AxesHelper(2));

    //Suelo
    var suelo = new THREE.Mesh(new THREE.PlaneGeometry(10,10,100,100), matSuelo);
    suelo.rotation.x = -Math.PI/2;
    suelo.receiveShadow = true;
    scene.add(suelo);

    //Texto
    var textLoader = new THREE.FontLoader();
    textLoader.load('fonts/helvetiker_regular.typeface.json', 
                    function(font){var geoText = new THREE.TextGeometry('A por el bote', 
                                                                        {
                                                                            size: 1, 
                                                                            height: 0.1, 
                                                                            curveSegments: 3, 
                                                                            font: font,
                                                                            weight: "bold",
                                                                            style: "normal",
                                                                            bevelThickness: 0.05,
                                                                            bevelSize: 0.04,
                                                                            bevelEnable: true
                                                                        });
                                    var texto = new THREE.Mesh(geoText, matCubo);
                                    scene.add(texto);
                                    texto.position.set(-2,0,1);
                                    texto.scale.set(0.5,0.5,0.5);
                    });
    //Modelo externo
    var loader = new THREE.ObjectLoader();
    loader.load('models/captain-america-shield-threejs/captain-america-shield.json',
                function(obj) {
                    obj.position.set(0,1,0);
                    cubo.add(obj);
                });

    //Habitación
    var shader = THREE.ShaderLib.cube;
    shader.uniforms.tCube.value = mapaEntorno;

    var matParedes = new THREE.ShaderMaterial(
        {
            fragmentShader: shader.fragmentShader,
            vertexShader: shader.vertexShader,
            uniforms: shader.uniforms,
            depthWrite: false,
            side: THREE.BackSide
        }
    );

    var habitacion = new THREE.Mesh(new THREE.BoxGeometry(30,30,30), matParedes);
    scene.add(habitacion);

    //Video
    //1. Crear el elemento de video en el documento
    video = document.createElement('video');
    video.src = "videos/Pixar.mp4";
    video.load();
    video.play();
    //2. Asociar la imagen del video a un canvas 2D
    videoImage = document.createElement('canvas');
    videoImage.width = 632;
    videoImage.height = 256;
    //3. Obtener un contexto para el canvas
    videoImageContext = videoImage.getContext('2d');
    videoImageContext. fillStyle = '0x0000AA';
    videoImageContext.fillRect(0, 0, videoImage.width, videoImage.height);
    //4. Crear textura a partir del canvas
    videoTexture = new THREE.Texture(videoImage);
    videoTexture.minFilter = THREE.LinearFilter;
    videoTexture.magFilter = THREE.LinearFilter;
    //5. Crear el material con la textura
    var movieMaterial = new THREE.MeshBasicMaterial({map:videoTexture, side:THREE.DoubleSide});
    //6. Objeto donde se pegará el video
    var movieScreen = new THREE.Mesh(new THREE.PlaneGeometry(30,9,4,4) , movieMaterial);
    movieScreen.position.set(0, 4.5, -5);
    scene.add(movieScreen);
}

function update()
{
    angulo += 0.01;
    cuboEsfera.rotation.y = angulo;

    //Actualizar el video
    if(video.readyState === video.HAVE_ENOUGH_DATA){
        videoImageContext.drawImage(video, 0, 0);
        if(videoTexture) videoTexture.needsUpdate = true;
    }
}

function render(){
    requestAnimationFrame(render);
    update();
    renderer.render(scene, camera);

}

